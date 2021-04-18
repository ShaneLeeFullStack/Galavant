 export default {
    name: 'autocomplete',
    props: {
        items: {
            type: Array,
            required: false,
            default: () => [],
        },
    },
    data() {
      return {
        search: '',
        results: [],
        isOpen: false,
      };
    },
    methods: {
        setResult(result) {
          this.search = result;
          this.isOpen = false;
      },
        onChange() {
            this.isOpen = true;
            this.filterResults();
        },
        filterResults() {
            this.results = this.items.filter(item => item.toLowerCase().indexOf(this.search.toLowerCase()) > -1);
        },
    },
  };