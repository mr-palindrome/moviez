from uuid import UUID
from collections import Counter
from urllib.parse import urlparse, parse_qs, urlencode
from tenacity import RetryError

from django.conf import settings
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status, viewsets, views
from rest_framework.exceptions import NotFound

from .service import third_party_api
from .models import Collection
from .serializers import CollectionSerializer, MovieSerializer


def construct_full_url(base_url, api_url):
    """
    Constructs the full URL by merging the base URL with the path and query parameters from the API URL.
    """
    api_parsed = urlparse(api_url)
    api_query = parse_qs(api_parsed.query)
    full_url = f"{base_url}"
    if api_query:
        query_string = urlencode(api_query, doseq=True)
        full_url = f"{full_url}/movies/?{query_string}"
    return full_url


class MovieAPIView(views.APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        url = settings.MOVIE_API_URL
        page_param = request.query_params.get("page")
        if page_param:
            try:
                page_param = int(page_param)
            except ValueError:
                return Response({"error": "Invalid page parameter"}, status=status.HTTP_400_BAD_REQUEST)
            url = f"{url}?page={page_param}"

        try:
            response_data = third_party_api.call_api(url=url, timeout=0.5)
            next_url = response_data.get("next")
            previous_url = response_data.get("previous")

            base_url = request.build_absolute_uri('/')[:-1]

            if next_url:
                response_data['next'] = construct_full_url(base_url, next_url)

            if previous_url:
                response_data['previous'] = construct_full_url(base_url, previous_url)

            return Response(response_data, status=status.HTTP_200_OK)

        except RetryError:
            return Response({"error": "Failed to retrieve data from third-party API after multiple attempts"},
                            status=status.HTTP_504_GATEWAY_TIMEOUT)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CollectionViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    model_class = Collection
    serializer_class = CollectionSerializer
    movie_serializer_class = MovieSerializer
    queryset = Collection.objects.all()
    lookup_field = 'uuid'

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)

    def get_object(self):
        uuid_str = self.kwargs.get(self.lookup_field)
        try:
            collection_uuid = UUID(uuid_str)
        except ValueError:
            raise NotFound(detail="Invalid UUID format")

        try:
            return Collection.objects.get(uuid=collection_uuid, user=self.request.user)
        except Collection.DoesNotExist:
            raise NotFound(detail="Collection not found")

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        collection_uuid = serializer.instance.uuid
        return Response({'collection_uuid': str(collection_uuid)}, status=status.HTTP_201_CREATED, headers=headers)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        collections_data = []
        genres_counter = Counter()

        for collection in queryset:
            collections_data.append({
                'title': collection.title,
                'uuid': str(collection.uuid),
                'description': collection.description
            })
            for movie in collection.movies.all():
                genres = movie.genres.split(',')
                genres_counter.update(genres)

        top_genres = [genre for genre, _ in genres_counter.most_common(3)]
        favourite_genres = ', '.join(top_genres)

        response_data = {
            'is_success': True,
            'data': {
                'collections': collections_data,
                'favourite_genres': favourite_genres
            }
        }
        return Response(response_data, status=status.HTTP_200_OK)
