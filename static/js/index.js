// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};

// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {
    app.data = {
    trip_reports: [],
    trip_reports_showing: false,
    this_report_showing: [],
    edit_this_report: null,
    substance_table: [],
  }

   app.toggle_trip_reports_showing = () => {
    app.vue.trip_reports_showing = !app.vue.trip_reports_showing;
  }

  app.toggle_this_report_showing = (report_id) => {
  // if index is already in this_report_showing, then remove it
      if(app.vue.edit_this_report == report_id){
          app.vue.edit_this_report = null
      }
      if(app.vue.this_report_showing.includes(report_id)){
          //this removes the desired report_id from the array
          let desiredindex = app.vue.this_report_showing.indexOf(report_id)
          app.vue.this_report_showing.splice(desiredindex,1)
      }else {
          app.vue.this_report_showing.push(report_id)
      }
  }


  app.fetch_trip_reports = () => {
      console.log("i make it to console")
      axios
          .get(fetch_trip_reports)
          .then((result) => {
              app.vue.trip_reports = result.data.trip_reports
          })
  }

  app.fetch_substance_table = () => {
      console.log("I am in fetch_substance_table")
      axios
          .get(fetch_substance_table)
          .then((result) => {
              app.vue.substance_table = result.data.substance_table
          })
  }

  app.edit_report = (report_id) => {
      if(app.vue.edit_this_report == report_id){
          app.vue.edit_this_report = null
      }
      else{ app.vue.edit_this_report = report_id}

      if(app.vue.this_report_showing.includes(report_id)) {
          //this removes the desired report_id from the array
          let desiredindex = app.vue.this_report_showing.indexOf(report_id)
          app.vue.this_report_showing.splice(desiredindex, 1)
      }
  }

  app.save_edited_report =(report_id) => {
      console.log(report_id)
      let report_index_intra =app.vue.trip_reports.findIndex(r => r.id === report_id)
      let edited_report = app.vue.trip_reports[report_index_intra]
      axios.post(update_report, {
          report_content: edited_report.report_content,
          id: edited_report.id,
      })
          .then((result) => {
          console.log("Received:", result.data);
          })

  }

  app.submit_trip_report = () => {
      console.log("we are in submit_trip_report")
      let new_trip_report = {
          report_id: null,
          title: "",
          substance: "",
          report_content: "",
          new_content: "",
          dif_headspace: null,
          anti_depress: null,
          is_showing: null,
      }
      axios.post((fetch_trip_reports), {
          is_showing: null,
          report_id: null,
      })
          .then((result) => {
              console.log(result)
              new_trip_report = {
                  report_id: result.data.id,
                  is_showing: null,
                  report_content: result.data.report_content,
              }
              console.log(result)
              app.vue.trip_reports.unshift(new_trip_report)
          })
  }

  app.define_new_substance = () => {
      let new_substance = {
          id: null,
          substance_name: "",
      }
      axios.post((fetch_substance_table), {
          id: null,
          substance_name: "",
      })
          .then((result) => {
              new_substance = {
                  id: result.data.id,
                  substance_name: result.data.substance_name
              }
              app.vue.substance_table.push(new_substance)
          })
  }

  app.delete_report = (report_id) => {
      let report_index_intra =app.vue.trip_reports.findIndex(r => r.id === report_id)
      let this_report = app.vue.trip_reports[report_index_intra]
      axios.post(delete_report, {
          id: this_report.id
      }).then(() => {
          app.vue.trip_reports.splice(report_index_intra,1)
      })
  }


      app.methods= {
       toggle_trip_reports_showing: app.toggle_trip_reports_showing,
       toggle_this_report_showing: app.toggle_this_report_showing,
       submit_trip_report: app.submit_trip_report,
       fetch_trip_reports: app.fetch_trip_reports,
       delete_report: app.delete_report,
       edit_report: app.edit_report,
       define_new_substance: app.define_new_substance,
       save_edited_report: app.save_edited_report,
       fetch_substance_table: app.fetch_substance_table,

   }

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        app.fetch_trip_reports()

    };

    // Call to the initializer.
    app.init();
};

init(app);
