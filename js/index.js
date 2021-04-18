// This will be the object that will contain the Vue attributes
// and be used to initialize it.
let app = {};
const genders = [ "Female","Male","Agender","Androgyne","Androgynous","Bigender",
    "Cis","Cisgender","Cis Female","Cis Male","Cis Man","Cis Woman","Cisgender Female",
    "Cisgender Male","Cisgender Man","Cisgender Woman","Female to Male","FTM","Gender Fluid",
    "Gender Nonconforming","Gender Questioning","Gender Variant","Genderqueer","Intersex",
    "Male to Female","MTF","Neither","Neutrois","Non-binary","Other","Pangender","Trans",
    "Trans*","Trans Female","Trans* Female","Trans Male","Trans* Male","Trans Man","Trans* Man",
    "Trans Person","Trans* Person","Trans Woman","Trans* Woman","Transfeminine","Transgender",
    "Transgender Female","Transgender Male","Transgender Man","Transgender Person","Transgender Woman",
    "Transmasculine","Transsexual","Transsexual Female","Transsexual Male","Transsexual Man",
    "Transsexual Person","Transsexual Woman",
    "Two-Spirit"]
const dosage_units_list= ["mcg (micrograms)", "mg (milligrams)", "g (grams)", "mL (milliliters)" ]
const substance_list= ["Magic Mushrooms", "Kava", "Salvia", "Ayahuasca", "Mescaline", "Sananga",
        "DMT", "Marijuana", "LSD", "Ketamine", "Cocaine"]
// Given an empty app object, initializes it filling its attributes,
// creates a Vue instance, and then initializes the Vue instance.
let init = (app) => {
    app.data = {
    add_substance: false,
    trip_reports: [],
    gender_list: [],
    dosage_units_list: [],
    trip_reports_showing: false,
    this_report_showing: [],
    edit_this_report: null,
    substance_list: [],
    exploring_safely: false,
    need_help: false,
    edit_this_profile_field: false,
    profile_fields: [],
    profile_updated: false,
    tags: []
  }

  app.toggle_add_substance = () => {
        app.vue.add_substance = !app.vue.add_substance;
  }

  app.fetch_doses = () => {
        app.vue.dosage_units_list = dosage_units_list;
  }

  app.fetch_substances = () => {
        app.vue.substance_list = substance_list;
  }

  app.fetch_genders = () => {
      app.vue.gender_list = genders;
  }

  app.fetch_my_trip_reports = () => {
      axios
          .get(fetch_trip_reports)
          .then((result) => {
              app.vue.trip_reports = result.data.trip_reports
          })
  }

  app.toggle_profile_updated = () => {
        app.vue.profile_updated =! app.vue.profile_updated;
  }

  app.toggle_edit_this_profile_field = () => {
        app.vue.edit_this_profile_field =! app.vue.edit_this_profile_field;
  }

   app.toggle_trip_reports_showing = () => {
    app.vue.trip_reports_showing = !app.vue.trip_reports_showing;
  }

  app.toggle_need_help = () => {
        app.vue.need_help = !app.vue.need_help
  }
  app.toggle_exploring_safely = () => {
        app.vue.exploring_safely = !app.vue.exploring_safely;
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


  app.toggle_edit_report = (report_id) => {
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

  app.submit_trip_report = () => {
      let new_trip_report = {
          report_id: null,
          title: "",
          substance: "",
          report_content: "",
          new_content: "",
          dif_headspace: null,
          anti_depress: null,
          at_festival: null,
          is_showing: null,
      }
      axios.post((fetch_trip_reports), {
          is_showing: null,
          report_id: null,
      })
          .then((result) => {
              new_trip_report = {
                  report_id: result.data.id,
                  is_showing: null,
                  report_content: result.data.report_content,
              }
              app.vue.trip_reports.unshift(new_trip_report)
          })
  }

  app.save_edited_report =(report_id) => {
      let report_index_intra =app.vue.trip_reports.findIndex(r => r.id === report_id)
      console.log(report_index_intra)
      let edited_report = app.vue.trip_reports[report_index_intra]
      console.log(edited_report.report_content)

      axios
          .post(update_report, {
          report_content: edited_report.report_content,
          id: edited_report.id,
      })
          .then((result) => {
          })
      app.fetch_tags()
  }

  app.fetch_profile_fields = () => {
      axios
          .get(fetch_profile_fields)
          .then((result) => {
              app.vue.profile_fields = result.data.profile_fields
          })
  }

  app.update_profile = () => {
        let updated_profile = {
            name: "",
            gender_identity: "",
            phone_number: "",
            city: "",
            tripsitter: null,
            safety_contact_name: "",
            safety_contact_phone_number: "",
        }
        axios.post((fetch_profile_fields), {
            tripsitter: null,
        })
            .then((result) => {
                updated_profile = {
                    name: result.data.name,
                    gender_identity: result.data.gender_identity,
                    phone_number: result.data.phone_number,
                    city: result.data.city,
                    safety_contact_name: result.data.safety_contact_name,
                    safety_contact_phone_number: result.data.safety_contact_phone_number,
                }
                app.vue.profile_fields.unshift(updated_profile)
            })
  }


  //The only purpose of this method is to make a javascript array version of the list of tags
  app.fetch_tags = () => {
      axios
          .get(fetch_tags)
          .then((result) => {
              app.vue.tags = result.data.user_report_tags
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
       toggle_add_substance: app.toggle_add_substance,
       toggle_trip_reports_showing: app.toggle_trip_reports_showing,
       toggle_this_report_showing: app.toggle_this_report_showing,
       submit_trip_report: app.submit_trip_report,
       fetch_my_trip_reports: app.fetch_my_trip_reports,
       delete_report: app.delete_report,
       toggle_edit_report: app.toggle_edit_report,
       save_edited_report: app.save_edited_report,
       toggle_exploring_safely: app.toggle_exploring_safely,
       toggle_need_help: app.toggle_need_help,
       toggle_profile_updated: app.toggle_profile_updated,
       fetch_profile_fields: app.fetch_profile_fields,
       fetch_genders: app.fetch_genders,
       fetch_substances: app.fetch_substances,
       fetch_tags: app.fetch_tags,
       fetch_doses: app.fetch_doses,


   }

    // This creates the Vue instance.
    app.vue = new Vue({
        el: "#vue-target",
        data: app.data,
        methods: app.methods
    });

    // And this initializes it.
    app.init = () => {
        app.fetch_doses(),
        app.fetch_substances()
        app.fetch_profile_fields(),
        app.fetch_genders(),
       app.fetch_my_trip_reports(),
        app.fetch_tags()
    };

    // Call to the initializer.
    app.init();
};

init(app);
