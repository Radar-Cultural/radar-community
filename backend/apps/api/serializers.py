from rest_framework import serializers
from rest_framework.reverse import reverse

from apps.accounts.models import OrganizationProfile
from apps.catalog.models import Audience, Category, Place
from apps.events.models import Event, EventScheduleItem
from apps.events.services.public_fields import public_admission_options, public_links
from apps.events.services.semantic import license_url


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

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['same_as'] = data['same_as'] or None
        return data


class OrganizationSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='official_name', read_only=True)
    same_as = serializers.ListField(source='authority_urls', read_only=True)
    verified = serializers.BooleanField(source='is_verified', read_only=True)

    class Meta:
        model = OrganizationProfile
        fields = ('id', 'name', 'slug', 'description', 'website', 'same_as', 'verified')

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['website'] = data['website'] or None
        return data


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
    admission_options = serializers.SerializerMethodField()
    links = serializers.SerializerMethodField()
    image = serializers.SerializerMethodField()
    language_code = serializers.SerializerMethodField()
    time_zone = serializers.SerializerMethodField()
    license_url = serializers.SerializerMethodField()
    schema_url = serializers.SerializerMethodField()
    rdf_url = serializers.SerializerMethodField()
    calendar_url = serializers.SerializerMethodField()

    class Meta:
        model = Event
        fields = (
            'id',
            'slug',
            'title',
            'summary',
            'description',
            'language_code',
            'time_zone',
            'starts_at',
            'ends_at',
            'event_status',
            'attendance_mode',
            'admission_type',
            'admission_options',
            'place',
            'location_details',
            'online_url',
            'organizer',
            'categories',
            'audiences',
            'schedule',
            'links',
            'image',
            'source_url',
            'description_license',
            'license_url',
            'schema_url',
            'rdf_url',
            'calendar_url',
            'updated_at',
        )

    def get_organizer(self, obj):
        if obj.organizer_id:
            if not obj.organizer.is_verified:
                return {'name': obj.organizer.official_name}
            return OrganizationSerializer(obj.organizer).data
        return {'name': obj.external_organizer_name}

    def get_language_code(self, obj):
        return obj.language_code or None

    def get_time_zone(self, obj):
        return obj.time_zone or None

    def get_image(self, obj):
        reusable_licenses = {Event.IMAGE_CC0, Event.IMAGE_CC_BY, Event.IMAGE_CC_BY_SA}
        if (
            not obj.include_image_in_open_data
            or not obj.image_url
            or obj.image_license not in reusable_licenses
        ):
            return None
        return {
            'url': obj.image_url,
            'license': obj.image_license,
            'credit': obj.image_credit,
            'source_url': obj.image_source_url,
        }

    def get_admission_options(self, obj):
        return public_admission_options(obj.admission_options)

    def get_links(self, obj):
        return public_links(obj.links)

    def get_license_url(self, obj):
        return license_url(obj.description_license)

    def get_schema_url(self, obj):
        return reverse('event-schema', kwargs={'slug': obj.slug}, request=self.context['request'])

    def get_rdf_url(self, obj):
        return reverse('event-rdf', kwargs={'slug': obj.slug}, request=self.context['request'])

    def get_calendar_url(self, obj):
        return reverse('event-calendar', kwargs={'slug': obj.slug}, request=self.context['request'])

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['online_url'] = data['online_url'] or None
        return data
