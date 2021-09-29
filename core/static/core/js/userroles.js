/*global $ */
"use strict";

var userroles = {
  // ------------------------------------------------------------------------
  // Users
  // ------------------------------------------------------------------------
  users: {
    index: function () {
      $("#user-table").DataTable({
        order: [],
        pageLength: 10,
        responsive: true,
        columnDefs: [
          {
            orderable: true,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".groups-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available groups",
        selectedListLabel: "Chosen groups",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });

      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  // ------------------------------------------------------------------------
  // Groups
  // ------------------------------------------------------------------------
  groups: {
    index: function () {
      $("#group-table").DataTable({
        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  // ------------------------------------------------------------------------

  genre: {
    index: function () {
      $("#genre-table").DataTable({
        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  // ------------------------------------------------------------------------

  newoffers: {
    index: function () {
      $("#offer-table").DataTable({
        order: [],
        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  // ----------------------------------------------------------------

  post: {
    index: function () {
      $("#post-table").DataTable({
        order: [],
        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  // ----------------------------------------------------------------

  category: {
    index: function () {
      $("#category-table").DataTable({
        order: [],
        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },
  // ----------------------------------------------------------------

  banner: {
    index: function () {
      $("#banner-table").DataTable({
        order: [],
        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  influenceroffer: {
    index: function () {
      $("#influenceroffer-table").DataTable({
        order: [],
        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  // ----------------------------------------------------------------

  subscriptionplans: {
    index: function () {
      $("#subscriptionplan-table").DataTable({
        order: [],

        pageLength: 10,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  //-------------------------------------------------------------------------
  credit: {
    index: function () {
      $("#credit-table").DataTable({
        order: [],

        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },
  //------------------------------------------------------------------------

  faq: {
    index: function () {
      $("#faq-table").DataTable({
        order: [],

        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  //------------------------------------------------------------------------
  creditorder: {
    index: function () {
      $("#creditorder-table").DataTable({
        order: [],

        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },
  //------------------------------------------------------------------------

  subscriptionorder: {
    index: function () {
      $("#subscriptionorder-table").DataTable({
        order: [],

        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },
  //-------------------------------------------------------------------------

  //------------------------------------------------------------------------

  contactusTab: {
    index: function () {
      $("#contactus-table").DataTable({
        order: [],

        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  //-------------------------------------------------------------------------
  category: {
    index: function () {
      $("#category-table").DataTable({
        order: [],

        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  //-------------------------------------------------------------------------

  // ------------------------------------------------------------------------

  planorder: {
    index: function () {
      $("#planorder-table").DataTable({
        order: [],

        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },
  },

  // -------------------------------------------------------------------

  transactionlog: {
    index: function () {
      $("#transactionlog-table").DataTable({
        order: [],

        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  // -------------------------------------------------------------------

  events: {
    index: function () {
      $("#event-table").DataTable({
        order: [],

        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  // ----------------------------------------------------------------------

  //---------------------------------------------------------------------

  // ----------------------------------------------------------------

  eventorder: {
    index: function () {
      $("#eventorder-table").DataTable({
        order: [],

        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  // ----------------------------------------------------------------

  agendas: {
    index: function () {
      $("#agenda-table").DataTable({
        order: [],

        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  //---------------------------------------------------------------------

  eventpracticeaudienceqa: {
    index: function () {
      $("#eventpracticeaudienceqa-table").DataTable({
        order: [],

        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  // -------------------------------------------------------------------

  eventclass: {
    index: function () {
      $("#eventclass-table").DataTable({
        order: [],

        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  Influencertransferredmoney: {
    index: function () {
      $("#Influencertransferredmoney-table").DataTable({
        order: [],

        pageLength: 25,
        responsive: true,
        columnDefs: [
          {
            orderable: false,
            targets: -1,
          },
        ],
      });
    },

    details: function () {
      $(".permissions-select").bootstrapDualListbox({
        nonSelectedListLabel: "Available user permissions",
        selectedListLabel: "Chosen user permissions",
        preserveSelectionOnMove: "moved",
        moveOnSelect: false,
      });
    },
  },

  // -------------------------------------------------------------------
};
