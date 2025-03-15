from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .serializers import TaskSerializer
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
from PIL import Image
from io import BytesIO


processor = TrOCRProcessor.from_pretrained(
    "microsoft/trocr-base-printed", use_fast=True)

model = VisionEncoderDecoderModel.from_pretrained(
    "microsoft/trocr-base-printed")


@api_view(["POST"])
def create_task_sync(request):
    serializer = TaskSerializer(data=request.data)

    if not serializer.is_valid():
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    task_type = serializer.validated_data["type"]

    match task_type:
        case "image-to-text-task":
            image_file = request.FILES["image"]

            try:
                image = Image.open(BytesIO(image_file.read())).convert("RGB")
            except Exception as e:
                return Response(
                    {"error": "Invalid image file"}, status=status.HTTP_400_BAD_REQUEST
                )

            try:
                pixel_values = processor(
                    image, return_tensors="pt").pixel_values

                generated_ids = model.generate(pixel_values)

                text = processor.batch_decode(
                    generated_ids, skip_special_tokens=True)[0]

                text = text.translate(str.maketrans("", "", "\n\r\t /"))
            except Exception as e:
                return Response(
                    {"error": "Internal server error"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

            return Response({"text": text}, status=status.HTTP_200_OK)
