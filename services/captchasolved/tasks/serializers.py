from rest_framework import serializers


class TaskSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=['image-to-text-task'])
    image = serializers.ImageField(
        required=False,
        allow_empty_file=False,
        help_text="Uploaded image file for image-to-text-task"
    )

    def validate(self, data):
        task_type = data.get("type")

        match task_type:
            case "image-to-text-task":
                if "image" not in data or not data["image"]:
                    raise serializers.ValidationError(
                        {"image": "This field is required for 'image-to-text-task'."}
                    )

        return data
