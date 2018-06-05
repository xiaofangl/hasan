/**
 * Created by xiaofangl on 2018/2/8.
 */
import Vue from 'vue'
import Vuex from 'vuex'
import routes from './routes'

Vue.use(Vuex);

const store = new Vuex.Store({
  state: {
    count: 0,
    activeName: '',
    tabs: ['001'],
    minHeight: '500px',
    message: []
  },

  mutations: {
    increment: state => state.count++,
    decrement: state => state.count--,
    addTab(state, tab) {
      if (state.tabs.indexOf(tab) === -1) {
        state.tabs.push(tab)
      }

      state.tabs.sort();
      state.activeName = tab
    },

    delTab(state, tab) {
      var i = state.tabs.indexOf(tab);
      if (i !== -1) {
        state.tabs.splice(i, 1)
      }
    },
    setActiveName(state, name) {
      state.activeName = name
    },
    setMinHeight(state, height) {
      state.minHeight = height
    },
    setMessage(state, item) {
      state.message.push(item)
    }
  },

  getters: {
    tabLabels: state => {
      var item = [];
      state.tabs.forEach(function (tab) {
        var i = routes.findIndex(function (route) {
          return route.name === tab
        });
        if (i !== -1) {
          item.push({name: tab, label: routes[i].label})
        }
      });

      return item
    },
    popMessage: state => {
      return state.message.shift()
    }
  }
});

export default store
