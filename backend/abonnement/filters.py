import django_filters
import django_filters.widgets
from creneau.models import Creneau
from django.db.models import Q
from django.shortcuts import get_object_or_404
from planning.models import Planning

from .models import Abonnement, AbonnementClient


class AbonnementClientFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method="universal_search", label="")
    # date_creation = django_filters.DateFromToRangeFilter(label="Date", lookup_expr='range', widget=django_filters.widgets.RangeWidget(attrs={'type': 'date'}))
    type_abonnement = django_filters.ModelChoiceFilter(
        queryset=Abonnement.objects.all(), label="Abonnement"
    )

    class Meta:
        model = AbonnementClient
        fields = ["search", "type_abonnement"]

    def universal_search(self, queryset, name, value):
        # print('Filter value:', value)
        # print('Initial queryset:', queryset)

        # Check if the search value is numeric (possibly an ID)
        if value.replace(".", "", 1).isdigit():
            queryset = queryset.filter(Q(client__id=value) | Q(client__carte=value))
        else:
            # Check if the search value matches any location names
            queryset = queryset.filter(
                Q(client__last_name__icontains=value)
                | Q(client__first_name__icontains=value)
                | Q(client__id__icontains=value)
            )

        print("Filtered queryset:", queryset.count())
        return queryset.distinct()


class CalenderFilter(django_filters.FilterSet):
    planning = django_filters.ModelChoiceFilter(
        queryset=Planning.objects.all(), label="Planning"
    )
    type_abonnement = django_filters.ModelChoiceFilter(
        queryset=Abonnement.objects.filter(actif=True),
        label="Abonnement",
        method="filter_by_abonnement_salles",
        required=False,
    )

    class Meta:
        model = Creneau
        fields = ["planning", "type_abonnement"]

    def __init__(self, *args, **kwargs):
        super(CalenderFilter, self).__init__(*args, **kwargs)
        items_data = "\n".join(f"{key} {value}" for key, value in self.data.items())
        print("SELF.data.items---------------------------------", items_data)
        if "planning" in self.filters:
            try:
                default_planning = Planning.objects.get(is_default=True)
                self.form.initial["planning"] = default_planning
                if not self.data:  # Apply filtering only if no user input
                    self.queryset = self.queryset.filter(planning=default_planning)
            except Planning.DoesNotExist:
                pass
        if "abc_id" in self.data:
            print("abc_id=========================", self.data.get("abc_id"))
            abc_id = int(self.data.get("abc_id"))
            abonnement_client = get_object_or_404(AbonnementClient, pk=abc_id)
            abonnement = Abonnement.objects.get(id=abonnement_client.type_abonnement.id)
            # self.form.initial['type_abonnement'] = abonnement
            self.data = self.data.copy()  # Make self.data mutable
            self.data["type_abonnement"] = abonnement.id
            planning = self.queryset.distinct("planning").first().planning
            print("The planning is=========================", planning)

            self.form.initial["planning"] = planning
            self.data["planning"] = planning
            # self.data['planning'] = abonnement.id
            # print('new selected abonnement', abonnement)
            print(
                "-----------------\n \n \n self.form.initial['type_abonnement'] \n \n",
                self.form.initial.items(),
            )
        else:
            print("NO ABCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")

    def filter_by_abonnement_salles(self, queryset, name, value):
        if value:
            salles = value.salles.all()
            queryset = queryset.filter(activity__salle__abonnements=value)
        return queryset


class CalenderFilterupdate(django_filters.FilterSet):
    planning = django_filters.ModelChoiceFilter(
        queryset=Planning.objects.all(), label="Planning"
    )
    type_abonnement = django_filters.ModelChoiceFilter(
        queryset=Abonnement.objects.filter(actif=True),
        label="Abonnement",
        method="filter_by_abonnement_salles",
        required=False,
    )

    class Meta:
        model = Creneau
        fields = ["planning", "type_abonnement"]

    def __init__(self, *args, **kwargs):
        super(CalenderFilterupdate, self).__init__(*args, **kwargs)
        items_data = "\n".join(f"{key} {value}" for key, value in self.data.items())
        print("SELF.data.items---------------------------------", items_data)

        if "abc_id" in self.data:
            print("abc_id=========================", self.data.get("abc_id"))
            abc_id = int(self.data.get("abc_id"))
            abonnement_client = get_object_or_404(
                AbonnementClient.objects.prefetch_related("creneaux"), pk=abc_id
            )
            abonnement = abonnement_client.type_abonnement
            self.data = self.data.copy()  # Make self.data mutable
            self.data["type_abonnement"] = abonnement.id

            abc_creneaux = abonnement_client.creneaux.all()
            creneau_pilote = (
                abc_creneaux.order_by("planning__id").distinct("planning__id").first()
            )
            print("The planning is=========================", creneau_pilote)

            if creneau_pilote:
                # self.data['planning'] = creneau_pilote.planning
                selected_planning = creneau_pilote.planning
                self.queryset = self.queryset.filter(planning=selected_planning)

                self.filters["planning"].queryset = Planning.objects.filter(
                    id=selected_planning.id
                )
                self.data["planning"] = selected_planning.id

            print(
                "-----------------\n \n \n self.form.initial['type_abonnement'] \n \n",
                self.form.initial.get("type_abonnement", None),
            )
        else:
            print("NO ABCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC")

    def filter_by_abonnement_salles(self, queryset, name, value):
        if value:
            salles = value.salles.all()
            queryset = queryset.filter(activity__salle__abonnements=value)
        return queryset
