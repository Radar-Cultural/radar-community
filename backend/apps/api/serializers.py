from rest_framework import serializers

from apps.accounts.models import OrganizationProfile
from apps.catalog.models import Audience, Category, Place
from apps.events.models import Event, EventScheduleItem


class CategorySerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'slug', 'description')


class AudienceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)

    class Meta:
        model = Audience
        fields = ('id', 'name', 'slug', 'description')


class PlaceSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    same_as = serializers.CharField(source='authority_url', read_only=True, allow_blank=True)

    class Meta:
        model = Place
        fields = (
            'id',
            'name',
            'slug',
            'kind',
            'address',
            'locality',
            'region',
            'country_code',
            'latitude',
            'longitude',
            'same_as',
        )


class OrganizationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='official_name', read_only=True)
    same_as = serializers.ListField(source='authority_urls', read_only=True)
    verified = serializers.BooleanField(source='is_verified', read_only=True)

    class Meta:
        model = OrganizationProfile
        fields = ('name', 'slug', 'website', 'same_as', 'verified')


class EventScheduleItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventScheduleItem
        fields = ('title', 'starts_at', 'ends_at', 'position')


class EventSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    place = PlaceSerializer(read_only=True)
    organizer = serializers.SerializerMethodField()
    categories = CategorySerializer(many=True, read_only=True)
    audiences = AudienceSerializer(many=True, read_only=True)
    schedule = EventScheduleItemSerializer(source='schedule_items', many=True, read_only=True)

    class Meta:
        model = Event
        fields = (
            'id',
            'slug',
            'title',
            'summary',
            'description',
            'starts_at',
            'ends_at',
            'event_status',
            'attendance_mode',
            'admission_type',
            'admission_options',
            'place',
            'online_url',
            'organizer',
            'categories',
            'audiences',
            'schedule',
            'links',
            'source_url',
            'updated_at',
        )

    def get_organizer(self, obj):
        if obj.organizer_id:
            return OrganizationSerializer(obj.organizer).data
        return {'name': obj.external_organizer_name}
