"""Views for commissions project"""
from django.shortcuts import render
from django.views.generic import TemplateView
# Create your views here.


class CommissionListView(TemplateView):
    """View to list commissions"""
    template_name = "commissions/commission_list.html"


class CommissionDetailView(TemplateView):
    """View to show commissions details"""
    template_name = "commissions/comission_detail.html"