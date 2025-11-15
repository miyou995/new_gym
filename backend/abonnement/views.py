import json

from client.models import Client
from django.contrib import messages
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils.translation import gettext as _
from django.views.decorators.http import require_POST
from django.views.generic import DeleteView
from transaction.models import Paiement

from abonnement.forms import (
    AbonnementClientAddForm,
    AbonnementClientEditForm,
    AbonnementClientUpdateRest,
)
from abonnement.mixins import CalendarAbonnementClientMixin

from .filters import CalenderFilterupdate
from .models import AbonnementClient, Creneau


def abc_htmx_view(request):
    client_id = request.GET.get("client")
    template_name = "abc_hx.html"
    abcs = AbonnementClient.objects.filter(client__id=client_id)
    response = render(request, template_name, {"abcs": abcs})
    response.headers = {"HX-Trigger": json.dumps({"referesh_creneaux": None})}
    return response


class CalendarAbonnementClient(PermissionRequiredMixin, CalendarAbonnementClientMixin):
    permission_required = "abonnement.add_abonnementclient"

    def get_template_names(self):
        template_name = "abonnement_calendar.html"
        return template_name

    def get_queryset(self):
        return Creneau.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["client"] = get_object_or_404(Client, pk=self.kwargs["pk"])
        return context


class RetreiveAbonnementClient(PermissionRequiredMixin, CalendarAbonnementClientMixin):
    permission_required = "abonnement.change_abonnementclient"
    filterset_class = CalenderFilterupdate
    model = Creneau

    def get_context_data(self, **kwargs):
        print("ABONNEMENT CLIENT RETREIVED==========================W")
        context = super().get_context_data(**kwargs)
        abc = get_object_or_404(AbonnementClient, pk=self.kwargs["pk"])
        context["abc"] = abc
        context["seleced_events"] = abc.get_selected_events()
        context["form"] = AbonnementClientEditForm(instance=abc)
        return context

    def get_filterset_kwargs(self, filterset_class):
        kwargs = super().get_filterset_kwargs(filterset_class)
        kwargs["data"] = self.request.GET.copy()
        kwargs["data"]["abc_id"] = self.kwargs["pk"]  # Inject abc_id into filter data
        return kwargs

    def get_queryset(self):
        selected_planning = None
        abc = get_object_or_404(AbonnementClient, pk=self.kwargs["pk"])
        creneau_pilote = (
            abc.creneaux.select_related("planning")
            .order_by("planning__id")
            .distinct("planning__id")
            .first()
        )
        ab_creneaux = Creneau.objects.filter(
            activity__salle__abonnements__id=abc.type_abonnement.id
        )
        if creneau_pilote:
            selected_planning = creneau_pilote.planning
        return ab_creneaux.filter(planning=selected_planning)

    def get_template_names(self):
        template_name = "snippets/update_calander.html"
        return template_name


@require_POST
def add_abonnement_client(request, client_pk, type_abonnement):
    form = AbonnementClientAddForm(request.POST, client_pk=client_pk)
    print("OUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
    if form.is_valid():
        print("Add abc Form is valid")
        form.save()
        message = _("Abonnement ajouter avec succès.")
        messages.success(request, str(message))
        return HttpResponse(
            status=204,
            headers={
                "HX-Trigger": json.dumps(
                    {"closeModal": "kt_modal", "refresh_abcs": None}
                )
            },
        )
    else:
        messages.error(request, form.errors)

        print("form.errores-------------->", form.errors)
    return redirect("abonnement:calendar_abonnement_client", kwargs={"pk": client_pk})


@require_POST
def update_abonnement_client(request, pk):
    abonnement_client = get_object_or_404(AbonnementClient, pk=pk)
    form = AbonnementClientEditForm(request.POST, instance=abonnement_client)
    print("OUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
    if form.is_valid():
        print("Add abc Form is valid")
        form.save()
        message = _("Abonnement ajouter avec succès.")
        messages.success(request, str(message))
        return HttpResponse(
            status=204,
            headers={
                "HX-Trigger": json.dumps(
                    {"closeModal": "kt_modal", "refresh_abcs": None}
                )
            },
        )
    else:
        messages.error(request, form.errors)

        print("form.errores-------------->", form.errors)
    return redirect("abonnement:calendar_abonnement_client", kwargs={"pk": pk})


class AbonnemtClientDeleteView(PermissionRequiredMixin, DeleteView):
    permission_required = "abonnement.delete_abonnementclient"
    model = AbonnementClient
    template_name = "buttons/delete.html"

    def get_success_url(self):
        return reverse_lazy(
            "client:client_detail", kwargs={"pk": self.object.client.pk}
        )

    def form_valid(self, form):
        success_url = self.get_success_url()
        paiment = Paiement.objects.filter(abonnement_client=self.object)
        if paiment:
            print("you can not delete this abc")
            messages.error(
                self.request,
                "Impossible de supprimer cet abonnement car il est lié à des paiements",
            )
            return HttpResponseRedirect(success_url)
        else:
            self.object.delete()
            print("GOOOOO")
            messages.success(self.request, "Abonnemet Client Supprimer avec Succés")
            return HttpResponseRedirect(success_url)


@require_POST
def update_date_paiement_rest(request, pk):
    if request.method == "POST":
        print(list(request.POST.items()))
        product = get_object_or_404(AbonnementClient, pk=pk)
        form = AbonnementClientUpdateRest(request.POST, instance=product)
        if form.is_valid():
            print("Form is valid. Data:", form.cleaned_data)
            form.save()
            message = _("Reste  updated successfully.")
            messages.success(request, str(message))
        else:
            message = _("Error occures when updating product.")
            messages.error(request, str(message))
        return HttpResponse(
            status=204,
            headers={
                "HX-Trigger": json.dumps(
                    {"closeModal": "kt_modal", "refresh_abcs": None}
                )
            },
        )


def renew_abonnement_client(request, pk):
    abonnement_client = get_object_or_404(AbonnementClient, pk=pk)
    renouvle_date = request.POST.get("renouvle")
    if renouvle_date:
        abonnement_client.renew_abc(renouvle_date)
    return HttpResponse(status=204)



def block_deblock_abonnement_client(request, pk):
    abonnement_client = get_object_or_404(AbonnementClient, pk=pk)
    block_date = request.POST.get("block_date")
    block_days = request.POST.get("block_days")
    print("block_date------------->>>>>", block_date)
    print("block_days------------->>>>>", block_days)
    if block_date:
        abonnement_client.lock(block_date, int(block_days))
        if not abonnement_client.is_locked:
            print("-----------------------blocking date not correct")
            message = _("vous pouvez pas bloquer cette abonnement.")
            messages.warning(request, str(message))
            return HttpResponse(
                status=204,
                headers={
                    "HX-Trigger": json.dumps(
                        {"closeModal": "kt_modal", "refresh_abcs": None}
                    )
                },
            )
        message = _("l'abonnement est bloqué.")
        messages.success(request, str(message))

    else:
        abonnement_client.unlock()
        message = _("l'abonnement est débloqué.")
        messages.success(request, str(message))
    return HttpResponse(
        status=204,
        headers={
            "HX-Trigger": json.dumps({"closeModal": "kt_modal", "refresh_abcs": None})
        },
    )
