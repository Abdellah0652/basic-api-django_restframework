from rest_framework import serializers
from .models import Customer, Profession, DataSheet, Document


# create serializers
class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        fields = ('id', 'dtype', 'doc_number', 'customer')


class DataSheetSerializer(serializers.ModelSerializer):
    class Meta:
        model = DataSheet
        fields = ('id', 'description', 'historical_data')


class ProfessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profession
        fields = ('id', 'description', 'status')


class CustomerSerializer(serializers.ModelSerializer):
    num_professions = serializers.SerializerMethodField()
    # had function 'StringRelatedField()' ktbyin smia f json dyal clé forienkey
    # data_sheet = serializers.StringRelatedField()
    # data_sheet = serializers.PrimaryKeyRelatedField(read_only=True)

    # hadi katst3mlha bach tbyin les row kamlin li kaynin f data_sheet fach kat3iyt 3la Customer
    data_sheet = DataSheetSerializer(read_only=True)
    professions = ProfessionSerializer(many=True)

    # had function 'StringRelatedField' katbyin smia d cle etranger ila kano 3ibara 3an list
    # ou katst3ml fach katkon ManyToManyField()
    # professions = serializers.StringRelatedField(many=True)
    # doc_num = serializers.StringRelatedField(many=True)
    document_set = DocumentSerializer(many=True, read_only=True)

    class Meta:
        model = Customer
        fields = ('id', 'name', 'address', 'professions', 'data_sheet', 'active',
                  'status_message', 'num_professions', 'document_set')

    def create(self, validated_data):
        professions = validated_data['professions']
        del validated_data['professions']

        customer = Customer.objects.create(**validated_data)
        for profession in professions:
            prof = Profession.objects.create(**profession)
            customer.professions.add(prof)
        customer.save()
        return customer

    def get_num_professions(self, obj):  # hadi mafhtmhach fdarss SerializerMethodField
        return obj.num_professions()

    def get_data_sheet(self, obj):
        return obj.data_sheet.description
