from django.db.models import F

from admin_site.models import SiteInfoModel
from django.contrib.auth.models import AnonymousUser
from django.shortcuts import redirect
# from communication.models import NoteModel, RecentActivityModel
# from communication.forms import NoteForm
from human_resource.models import StaffModel, StaffProfileModel
# from pharmacy.models import DrugVariantModel


def general_info(request):
    site_info = SiteInfoModel.objects.first()

    return {
        'site_info': site_info,
    }
