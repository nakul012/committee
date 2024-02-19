# from rest_framework import serializers
# from profiles.models import *
# from profiles.utils import change_student_room


# class ChangeRoomSerializer(serializers.Serializer):
#     old_room_id = serializers.IntegerField()
#     new_room_id = serializers.IntegerField()
#     student_id = serializers.IntegerField()

#     def create(self, validated_data):
#         old_room_id = validated_data['old_room_id']
#         new_room_id = validated_data['new_room_id']
#         student_id = validated_data['student_id']
#         new_seat_history = change_student_room(student_id=student_id, old_room_id=old_room_id, new_room_id=new_room_id)
#         return new_seat_history