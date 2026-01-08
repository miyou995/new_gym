import django_filters
import django_filters.widgets
from planning.models import Planning
from salle_activite.models import Salle

from .models import Creneau


class CalenderFilterCreneau(django_filters.FilterSet):
    planning = django_filters.ModelChoiceFilter(
        queryset=Planning.objects.all(), label="Planning"
    )
    activity__salle = django_filters.ModelChoiceFilter(
        queryset=Salle.objects.all(), label="Abonnement"
    )

    class Meta:
        model = Creneau
        fields = ["planning", "activity__salle"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if "planning" in self.filters:
            try:
                default_planning = Planning.objects.get(is_default=True)
                self.form.initial["planning"] = default_planning
                if not self.data:
                    self.queryset = self.queryset.filter(planning=default_planning)
            except Planning.DoesNotExist:
                pass
