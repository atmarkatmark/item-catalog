<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <h1><img src="@/assets/logo.png"/>Mobile Battery Central</h1>
      </v-col>
    </v-row>

    <v-row class="text-center">
      <v-col cols="12">
        <v-data-table
          :headers="headers"
          :items="items"
          dark
          items-per-page=50>
        </v-data-table>
      </v-col>
    </v-row>

    <v-row class="text-center">
      <v-col cols="6">
        <v-btn class="primary" @click="load">Load</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import items from '@/assets/data.json';
  
  export default {
    name: 'Table',

    data: function () {
      return {
        headers: [
          {
            text: '販売元',
            align: 'start',
            sortable: true,
            value: 'manufacture'
          },
          {
            text: '名称',
            align: 'start',
            sortable: true,
            value: 'name'
          },
          {
            text: '型番',
            align: 'start',
            sortable: true,
            value: 'model'
          },
          {
            text: '税込価格',
            align: 'right',
            sortable: true,
            value: 'price'
          }
        ],

        items: items
      }
    },

    methods: {
      load: function () {
        // axios.get('@/assets/data.json').then(res => console.log(res))
        console.log(items)
      }
    }
  }
</script>
