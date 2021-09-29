# -*- coding: utf-8 -*-

from django.urls import path, include
from django.views.generic import TemplateView
from . import views
app_name = "core"

urlpatterns = [

    path("", TemplateView.as_view(template_name="core/home.html"), name="index"),

    # User
    path("users/", views.UserListView.as_view(), name="user-detail"),

    path("users/", views.UserListView.as_view(), name="user-list"),
    path("users/create/", views.UserCreateView.as_view(), name="user-create"),
    path("users/<int:pk>/update/", views.UserUpdateView.as_view(), name="user-update"),
    path("users/<int:pk>/delete/", views.UserDeleteView.as_view(), name="user-delete"),
    path("users/<int:pk>/password/", views.UserPasswordView.as_view(), name="user-password"),
    path("ajax-users", views.UserAjaxPagination.as_view(), name="user-list-ajax"),
]
 
urlpatterns += [
 
    #plan
    path("subscription-plan/", views.SubscriptionPlanListView.as_view(), name="subscriptionplan-list"),
    path("subscription-plan/create/", views.SubscriptionPlanCreateView.as_view(), name="subscriptionplan-create"),
    path("subscription-plan/<int:pk>/update/", views.SubscriptionPlanUpdateView.as_view(), name="subscriptionplan-update"),
    path("subscription-plan/<int:pk>/delete/", views.SubscriptionPlanDeleteView.as_view(), name="subscriptionplan-delete"),
    path("ajax-subscription-plan", views.SubscriptionPlanAjaxPagination.as_view(), name="subscriptionplan-list-ajax"),
   
    #offer

    path("offer/", views.OfferListView.as_view(), name="offer-list"),
    path("offer/create/", views.OfferCreateView.as_view(), name="offer-create"),
    path("offer/<int:pk>/update/", views.OfferUpdateView.as_view(), name="offer-update"),
    path("offer/<int:pk>/delete/", views.OfferDeleteView.as_view(), name="offer-delete"),
    path("ajax-offer", views.OfferAjaxPagination.as_view(), name="offer-list-ajax"),

    # Banner
    path("banner/", views.BannerListView.as_view(), name="banner-list"),
    path("banner/create/", views.BannerCreateView.as_view(), name="banner-create"),
    path("banner/<int:pk>/update/", views.BannerUpdateView.as_view(), name="banner-update"),
    path("banner/<int:pk>/delete/", views.BannerDeleteView.as_view(), name="banner-delete"),
    path("ajax-banner", views.BannerAjaxPagination.as_view(), name="banner-list-ajax"),

    # faq
    
    path("faq/", views.FaqListView.as_view(), name="faq-list"),
    path("faq/create/", views.FaqCreateView.as_view(), name="faq-create"),
    path("faq/<int:pk>/update/", views.FaqUpdateView.as_view(), name="faq-update"),
    path("faq/<int:pk>/delete/", views.FaqDeleteView.as_view(), name="faq-delete"),
    path("ajax-faq", views.FaqAjaxPagination.as_view(), name="faq-list-ajax"),

    # credit
    
    path("credit/", views.CreditListView.as_view(), name="credit-list"),
    path("credit/create/", views.CreditCreateView.as_view(), name="credit-create"),
    path("credit/<int:pk>/update/", views.CreditUpdateView.as_view(), name="credit-update"),
    path("credit/<int:pk>/delete/", views.CreditDeleteView.as_view(), name="credit-delete"),
    path("ajax-credit", views.CreditAjaxPagination.as_view(), name="credit-list-ajax"),

    # credit order

    path("credit-order/", views.CreditOrderListView.as_view(), name="credit-order-list"),
    path("ajax-credit", views.CreditOrderAjaxPagination.as_view(), name="creditorder-list-ajax"),
    
    # contact us

    path("contactus/", views.ContactUsListView.as_view(), name="contactus-list"),
    path("ajax-contactus", views.ContactUsAjaxPagination.as_view(), name="contactus-list-ajax"),

    # subscription order

    path("subscriptionorder/", views.SubscriptionOrderListView.as_view(), name="subscriptionorder-list"),
    path("ajax-subscriptionorder", views.SubscriptionOrderAjaxPagination.as_view(), name="subscriptionorder-list-ajax"),

    # influencer category

    path("category/", views.CategoryListView.as_view(), name="category-list"),
    path("category/create/", views.CategoryCreateView.as_view(), name="category-create"),
    path("category/<int:pk>/update/", views.CategoryUpdateView.as_view(), name="category-update"),
    path("category/<int:pk>/delete/", views.CategoryDeleteView.as_view(), name="category-delete"),
    path("ajax-category", views.CategoryAjaxPagination.as_view(), name="category-list-ajax"),


    # event

    path("event/", views.EventListView.as_view(), name="event-list"),
    path("event/create/", views.EventCreateView.as_view(), name="event-create"),
    path("event/<int:pk>/update/", views.EventUpdateView.as_view(), name="event-update"),
    path("event/<int:pk>/delete/", views.EventDeleteView.as_view(), name="event-delete"),
    path("ajax-event", views.EventAjaxPagination.as_view(), name="event-list-ajax"),

    # event order

    path("eventorder/", views.EventOrderListView.as_view(), name="eventorder-list"),
    path("ajax-eventorder", views.EventOrderAjaxPagination.as_view(), name="eventorder-list-ajax"),

   # event agenda

    path("agenda/", views.AgendaListView.as_view(), name="agenda-list"),
    path("agenda/create/", views.AgendaCreateView.as_view(), name="agenda-create"),
    path("agenda/<int:pk>/update/", views.AgendaUpdateView.as_view(), name="agenda-update"),
    path("agenda/<int:pk>/delete/", views.AgendaDeleteView.as_view(), name="agenda-delete"),
    path("ajax-agenda", views.AgendaAjaxPagination.as_view(), name="agenda-list-ajax"),


    # event agenda

    path("eventpracticeaudienceqa/", views.EventPracticeAudienceQAListView.as_view(), name="eventpracticeaudienceqa-list"),
    path("eventpracticeaudienceqa/create/", views.EventPracticeAudienceQACreateView.as_view(), name="eventpracticeaudienceqa-create"),
    path("eventpracticeaudienceqa/<int:pk>/update/", views.EventPracticeAudienceQAUpdateView.as_view(), name="eventpracticeaudienceqa-update"),
    path("agenda/<int:pk>/delete/", views.EventPracticeAudienceQADeleteView.as_view(), name="eventpracticeaudienceqa-delete"),
    path("ajax-eventpracticeaudienceqa", views.EventPracticeAudienceQAAjaxPagination.as_view(), name="eventpracticeaudienceqa-list-ajax"),


    # influenceroffer

    path("influenceroffer/", views.InfluencerOfferListView.as_view(), name="influenceroffer-list"),
    path("influenceroffer/create/", views.InfluencerOfferCreateView.as_view(), name="influenceroffer-create"),
    path("influenceroffer/<int:pk>/update/", views.InfluencerOfferUpdateView.as_view(), name="influenceroffer-update"),
    path("influenceroffer/<int:pk>/delete/", views.InfluencerOfferDeleteView.as_view(), name="influenceroffer-delete"),
    path("ajax-influenceroffer", views.InfluencerOfferAjaxPagination.as_view(), name="influenceroffer-list-ajax"),

    # transactionlog
    
    path("transactionlog/", views.TransactionlogListView.as_view(), name="transactionlog-list"),
    path("ajax-transactionlog", views.TransactionlogAjaxPagination.as_view(), name="transactionlog-list-ajax"),

    # eventclass

    path("eventclass/", views.EventClassListView.as_view(), name="eventclass-list"),
    path("eventclass/create/", views.EventClassCreateView.as_view(), name="eventclass-create"),
    path("eventclass/<int:pk>/update/", views.EventClassUpdateView.as_view(), name="eventclass-update"),
    path("eventclass/<int:pk>/delete/", views.EventClassDeleteView.as_view(), name="eventclass-delete"),
    path("ajax-eventclass", views.EventClassAjaxPagination.as_view(), name="eventclass-list-ajax"),

    path("Influencertransferredmoney/", views.InfluencerTransferredMoneyListView.as_view(), name="Influencertransferredmoney-list"),
    path("ajax-influencertransferredmoney", views.InfluencerTransferredMoneyAjaxPagination.as_view(), name="influencertransferredmoney-list-ajax"),

    path("run_transfer_fund/", views.run_transfer_fund, name="run_transfer_fund-list"),


    # Blogpost From blog page
    path("blogpost/", views.BlogpostListView.as_view(), name="post-list"),
    path("blogpost/create/", views.BlogpostCreateView.as_view(), name="post-create"),
    path("blogpost/<int:pk>/update/", views.BlogpostUpdateView.as_view(), name="post-update"),
    path("blogpost/<int:pk>/delete/", views.BlogpostDeleteView.as_view(), name="post-delete"),
    path("ajax-blogpost", views.BlogpostAjaxPagination.as_view(), name="post-list-ajax"),

    #Blogcategory From blog page
    path("blogcategory/", views.BlogcategoryListView.as_view(), name="category-list"),
    path("blogcategory/create/", views.BlogcategoryCreateView.as_view(), name="category-create"),
    path("blogcategory/<int:pk>/update/", views.BlogcategoryUpdateView.as_view(), name="category-update"),
    path("blogcategory/<int:pk>/delete/", views.BlogcategoryDeleteView.as_view(), name="category-delete"),
    path("ajax-blogcategory", views.BlogcategoryAjaxPagination.as_view(), name="category-list-ajax"),
]

 