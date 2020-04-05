<template>
  <v-app>
    <v-app-bar
      app
      color="primary"
      dark
    >
      <div class="d-flex align-center">
        モバイルバッテリカタログ
      </div>

      <v-spacer></v-spacer>

      <v-btn
        href="https://kuratsuki.net/"
        target="_blank"
        text
      >
        <span class="mr-2">くらつきねっと</span>
        <v-icon>mdi-open-in-new</v-icon>
      </v-btn>
    </v-app-bar>

    <v-content>
      <Table/>
    </v-content>
  </v-app>
</template>

<script>
import Table from './components/Table';

export default {
  name: 'App',

  components: {
    Table
  },

  data: () => ({
    //
  }),
};
</script>
