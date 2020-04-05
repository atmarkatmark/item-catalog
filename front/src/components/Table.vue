<template>
  <v-container>
    <v-row class="text-center">
      <v-col cols="12">
        <h1>Mobile Battery Catalog</h1>
      </v-col>
    </v-row>

    <v-row class="item-card">
      <v-col cols="4" sm="12" md="6">
        <ItemCard :item="selected_item"></ItemCard>
      </v-col>

      <v-col cols="8" sm="12" md="6">
        <!-- 表部分 -->
        <v-data-table
          :headers="headers"
          :items="items"
          dark
          multi-sort
          :items-per-page=50
          @click:row="show_item">
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
  import items from '@/assets/data.json';
  import ItemCard from '@/components/ItemCard';
  
  export default {
    name: 'Table',

    components: {
      ItemCard
    },

    data: function () {
      return {
        selected_item: {},

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
            text: '容量(mAh)',
            align: 'right',
            sortable: true,
            value: 'capacity'
          },
          {
            text: 'PD最大出力',
            align: 'start',
            sortable: true,
            value: 'pd_w'
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
        // console.log(items)
      },

      show_item: function (item) {
        this.selected_item = item
        // console.log(item)
      }
    }
  }
</script>
