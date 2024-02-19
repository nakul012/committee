from rest_framework import serializers
from .models import *
# from profiles.utils import change_student_room


class AssignCommitteeSerializer(serializers.Serializer):
    level_type = serializers.IntegerField()
    type_of_committee = serializers.IntegerField()
    role = serializers.IntegerField()
    count = serializers.IntegerField()
    department = serializers.IntegerField()
    category_of_employee = serializers.IntegerField()
    designation = serializers.IntegerField()

    def create(self, validated_data):
        old_room_id = validated_data['old_room_id']
        new_room_id = validated_data['new_room_id']
        student_id = validated_data['student_id']
        # new_seat_history = change_student_room(student_id=student_id, old_room_id=old_room_id, new_room_id=new_room_id)
        return 