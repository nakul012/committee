from rest_framework import serializers
from .models import MasterConfig
from rest_framework import status, response, exceptions, views
from auth_app.common.errors import ClientErrors


class MasterConfigSerializer( serializers.ModelSerializer,):
    children = serializers.SerializerMethodField()
    

    
    class Meta:
        model = MasterConfig
        fields = ['id', 'label', 'max_subcategory_level', 'children',"parent"]
        # exclude = ('created_at', 'updated_at')

    

    def validate(self, data):
        if not data.get("label"):
            raise exceptions.ValidationError('Measurement with this profile name already exists.')
		
        # if MasterConfig.objects.filter(label=data.get("label","")).exists():
        #     raise ClientErrors("This label is already exists")

        return super().validate(data)
    def create(self, validated_data):
        parent=validated_data.get("parent",None)
        
        if parent is not None:
            try:
                parent_category = MasterConfig.objects.get(id=parent.id)

                if parent_category.max_subcategory_level <= parent_category.children.count():
                    raise serializers.ValidationError("Maximum subcategory level reached for the parent category.")
                validated_data['parent'] = parent_category  # Set the parent field
            except MasterConfig.DoesNotExist:
                raise serializers.ValidationError("Parent category does not exist.")
        else:
            parent_category = None
       
        # Create the new MasterConfig instance with the parent set
        return super().create(validated_data)

    
    def get_children(self, instance):
        children = instance.children.all()
        children_serializer = MasterConfigSerializer(children, many=True)
        return children_serializer.data
    
    # def get_children(self, obj):
    #     import ipdb;
    #     ipdb.set_trace()
    #     children_qs = obj.children.all()
    #     children_serializer = self.__class__(children_qs, many=True)
    #     return children_serializer.data

class ConfigSerializer( serializers.ModelSerializer,):
    

    
    class Meta:
        model = MasterConfig
        fields = ['id', 'label', 'max_subcategory_level', "parent"]
        # exclude = ('created_at', 'updated_at')

    

    def validate(self, data):
        if not data.get("label"):
            raise exceptions.ValidationError('Measurement with this profile name already exists.')
		
        if MasterConfig.objects.filter(label=data.get("label","")).exists():
            raise ClientErrors("This label is already exists")

        return super().validate(data)
    def create(self, validated_data):
        parent=validated_data.get("parent",None)
        
        if parent is not None:
            try:
                parent_category = MasterConfig.objects.get(id=parent.id)

                if parent_category.max_subcategory_level <= parent_category.children.count():
                    raise serializers.ValidationError("Maximum subcategory level reached for the parent category.")
                validated_data['parent'] = parent_category  # Set the parent field
            except MasterConfig.DoesNotExist:
                raise serializers.ValidationError("Parent category does not exist.")
        else:
            parent_category = None
       
        # Create the new MasterConfig instance with the parent set
        return super().create(validated_data)

    
