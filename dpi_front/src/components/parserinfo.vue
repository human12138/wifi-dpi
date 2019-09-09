<template>
  <div>
    <h1>STA记录</h1>
    <Divider />
    <div id="d1">
      <div style="padding: 20px width:30%">
      <Card>
          <p slot="title" style="height:40px">
            <Icon type="ios-person"/>
            STA基本信息
            </p>
          <table style="text-align:left">
            <tr v-for="sta in sta_info"><td>{{sta.info_name}}</td><td>{{sta.info_data}}</td></tr>
            <tr><td>操作:</td>
              <td><Button id='name' @click="choose_ap" type="primary">切换AP</Button>
                <Modal v-model="modal1"
                title="选择AP"
                @on-ok="ok">
                <Table :columns="ap_col" :data="ap_data1"></Table>
                </Modal>
              </td></tr>
            <tr>
              <td>查询日期范围:</td>
              <td>
                <p v-model="showdate">{{showdate}}
                <Dropdown @on-click="datechoose" trigger="custom" :visible="visible">
                  <a href="javascript:void(0)" @click="dropopen">
                      选择范围
                      <Icon type="ios-arrow-down"></Icon>
                  </a>
                  <DropdownMenu slot="list">
                      <DropdownItem name='1'>一周</DropdownItem>
                      <DropdownItem name='2'>一个月</DropdownItem>
                      <DropdownItem name='3'>三个月</DropdownItem>
                      <DropdownItem name='4'>六个月</DropdownItem>
                      <DropdownItem name='5'>一年</DropdownItem>
                      <DropdownItem name='6'>
                        <DatePicker
                          :open="open"
                          :value="value3"
                          confirm
                          type="daterange"
                          @on-change="handleChange"
                          @on-clear="handleClear"
                          @on-clickoutside='handleClear'
                          @on-ok="handleOk"
                          v-model="dates">
                          <a href="javascript:void(0)" @click='handleClick'>
                              <Icon type="ios-calendar-outline"></Icon>
                              <template>自定义范围</template>
                          </a>
                        </DatePicker>
                      </DropdownItem>
                  </DropdownMenu>
                </Dropdown>
              </p></td></tr>
          </table>
          <Divider />
          <Table :columns='ip_col' :data='ip_data' :size='small':width='200' :height='200'></Table>
      </Card>
    </div>
      <Tabs type='card' value="network" @on-click="choose_layer" style="width: 30%;height: 400px;display: inline-block;">
        <TabPane label="网络层统计" name="network"><div :class="className" :id="id" :style="{margin:margin,height:height,width:width}" ref="desEchart"></div></TabPane>
        <TabPane label="传输层统计" name="transport"><div :class="className" :id="id" :style="{margin:margin,height:height,width:width}" ref="portEchart"></div></TabPane>
        <TabPane label="应用层统计" name="application"><div id="protocol" style="width: 400px;height: 300px;display: inline-block;"></div></TabPane>
      </Tabs>
      <div style="width: 40%;height: 400px;display: inline-block;">
        <Table border :height='400' :columns="ap_col1" :data="ap_data1" :stripe=true  :size="small"></Table>
      </div>
      <!--Table :columns="columnsimg" :data="dataimg" style = "width:700px" :show-header=false default></Table>-->
    </div>
    <Divider><h2>应用层深度分析</h2></Divider>
    <Select v-model="paroto_model" style="width:200px" placeholder='选择要解析的协议' @on-change='choose_proto'>
        <Option v-for="item in protoList" :value="item.value" :key="item.value">{{ item.label }}</Option>
    </Select>
    <Divider><h2>包数据记录</h2></Divider>
    <Table border :columns="columns1" :data="data1" default></Table>
    <Page :total="count" show-elevator @on-change='change_page'/>
  </div>
</template>
<style>
.echartLayout {
   margin: auto;
   position: center;
   width:30%;
   height:30%;

 }
#d2{
     display: -webkit-flex;
     display: flex;
     justify-content: space-around;
     height: 10%
 }
#d1{
    display: -webkit-flex;
    display: flex;
    justify-content: space-around;
}
</style>
<script>
import echarts from 'echarts'
export default {
  props: {
    className: {
      type: String,
      default: 'yourClassName'
    },
    id: {
      type: String,
      default: 'yourID'
    },
    width: {
      type: String,
      default: '400px'
    },
    height: {
      type: String,
      default: '300px'
    },
    float: {
      type: String,
      default: 'left'
    },
    margin:{
      type: String,
      default: 'center'
    }
  },
  mounted() {
    this.getdata(this.$route.query.ip,this.$route.query.mac,this.$route.query.start_date,this.$route.query.stop_date);
    //this.draw_protocol('protocol');
    //this.drawDes();
    //this.drawport();
    //this.draw_website('website');
    //this.draw_protocol('protocol');
    //this.initEchart('container');
  },
  beforeDestroy() {
    if (!this.chart) {
      return
    }
    this.chart.dispose();
    this.chart = null;
  },
  data () {
    return {
      count: '',
      isRouterAlive: true,
      modal1:false,
      visible: false,
      dates: '',
      open: false,
      value3: '',
      showdate: '一周内',
      name1 :1,
      ip : this.$route.query.ip,
      mac : this.$route.query.mac,
      ap_mac:this.$route.query.ap_mac,
      start_date: this.$route.query.start_date,
      stop_date: this.$route.query.stop_date,
      /*
      columnsimg : [
        {
        key:'url1',
        render: (h,params)=>{
          return h('img',{
            attrs:{
              src: params.row.url1,
              style: 'width:140px;'//border-radius:2px;'
            },
          });
        }
      },
      {
        key:'url2',
        render: (h,params)=>{
          return h('img',{
            attrs:{
              src: params.row.url2,
              style: 'width:140px;'//border-radius:2px;'
            },
          });
        },
      },
      {
        key:'url3',
        render: (h,params)=>{
          return h('img',{
            attrs:{
              src: params.row.url3,
              style: 'width:140px;'//border-radius:2px;'
            },
          });
        },
      },
      {
        key:'url4',
        render: (h,params)=>{
          return h('img',{
            attrs:{
              src: params.row.url4,
              style: 'width:140px;'//border-radius:2px;'
            },
          });
        },
      },
      {
        key:'url5',
        render: (h,params)=>{
          return h('img',{
            attrs:{
              src: params.row.url5,
              style: 'width:140px;'//border-radius:2px;'
            },
          });
        }
      }
    ],*/
    protoList:[
      {
        value: 'ALL',
        label: '全部',
      },
      {
        value:'DNS',
        label:'DNS',
      },
      {
        value: 'HTTP',
        label: 'HTTP',
      },
      {
        value: 'SMTP',
        label: 'SMTP',
      },
    ],
    ap_col:[
      {
        title: 'AP名称',
        key: 'name',
        tooltip:true
      },
      {
        title: 'MAC地址',
        key: 'mac',
        tooltip:true
      },
      {
        title: '最后连接时间',
        key: 'date',
        tooltip:true
      },
    ],
    ip_col:[
      {
        title: '曾使用的IP地址',
        key: 'ip_history'
      }
    ],
    ap_col1: [
      {
        title: '曾连接的AP列表',
        align: 'center',
        children:[
          {
            title: 'AP名称',
            key: 'name',
            tooltip:true
          },
          {
            title: 'MAC地址',
            key: 'mac',
            tooltip:true
          },
          {
            title: '最后连接时间',
            key: 'date',
            tooltip:true
          },
          {
            title: '查看AP详情',
            key: 'action',
            width: '100',
            align: 'center',
            render: (h,params)=>{
              return h('div',{
                props:{
                  id: 'd1'
                }
              },
              [
              h('Button',{
                props:{
                  type: 'text',
                  size: 'small'
                },
                on:{
                  click: ()=>{
                    //this.ip_detail(params.index)
                  }
                }
              },'历史'),
              h('Button',{
                props:{
                  type: 'text',
                  size: 'small'
                },
                on:{
                  click: ()=>{
                    //this.ip_detail(params.index)
                  }
                }
              },'实时')
            ]);
          }
          }
        ]
      }
      ],
      /*
      ip_data:[
        {ip_history:'192.168.126.2'},
        {ip_history:'192.168.126.3'},
        {ip_history:'192.168.126.4'},
        {ip_history:'192.168.126.5'},
        {ip_history:'192.168.126.6'},
      ] ,
      ap_data1:[
        {date: '2019-06-19 23:13:52',mac:'34:23:87:A9:26:9B',name:'xd_stu'},
        {date: '2019-06-19 23:13:52',mac:'D4:EE:07:32:01:5A',name:'xd_stu'},
        {date: '2019-06-19 23:13:52',mac:'D4:EE:07:32:01:5A',name:'xd_stu'},
        {date: '2019-06-19 23:13:52',mac:'D4:EE:07:32:01:5A',name:'xd_stu'},
        {date: '2019-06-19 23:13:52',mac:'D4:EE:07:32:01:5A',name:'xd_stu'},
        {date: '2019-06-19 23:13:52',mac:'D4:EE:07:32:01:5A',name:'xd_stu'},
      ],
      ap_data: [{
        name: 'xd_stu',
        value: 'D4:EE:07:32:01:5A',
        children: [
          {
            name:'D4:EE:07:32:01:5A',
            value: '192.168.3.1'
          },
          {
            name:'D4:EE:07:32:01:5A',
            label:{
              color:'green'
            }
          },
          {
            name:'D4:EE:07:32:01:5A',
          },
          {
            name:'D4:EE:07:32:01:5A'
          },
          {
            name:'D4:EE:07:32:01:5A'
          },
          {
            name:'D4:EE:07:32:01:5A'
          },
          {
            name:'D4:EE:07:32:01:5A'
          },
        ]
      }],
/*
      dataimg:[
        {
          url1:'/src/assets/1.jpg',
          url2:"../assets/2.jpg",
          url3:"../assets/3.jpg",
          url4:"../assets/4.jpg",
          url5:"../assets/5.jpg"
        },
        {
          url1: "../assets/6.png",
          url2: "../assets/5.jpg",
          url3: "../assets/1.jpg",
          url4: "../assets/3.jpg",
          url5: "../assets/6.png"
        }
      ],*/
      sta_info:[
        {
          info_name: 'MAC地址:',
          info_data: '34:23:87:A9:26:9B'
        },
        {
          info_name: '所属AP的名称:',
          info_data: 'xd_stu'
        },
        {
          info_name: '所属AP的MAC',
          info_data: 'D4:EE:07:32:01:5A'
        },
      ],
      /*
      desdata_x :  [10, 52, 200, 334, 390, 330, 220,10, 52, 200],
      desdata_y :  ['192.168.199.126', '192.168.199.124', '192.168.1.3', '192.168.1.2',
      '192.168.3.6','192.168.199.103', '192.168.3.1','192.168.3.6','192.168.199.103', '192.168.3.1'],
      website_label: ['baidu', 'bilibili', 'neteasy', 'iqiyi', 'qq','baidu1', 'bilibili1', 'neteasy1', 'iqiyi1', 'qq1'],
      website_data: [
        {value: 335, name: 'baidu'},
        {value: 310, name: 'neteasy'},
        {value: 234, name: 'iqiyi'},
        {value: 135, name: 'qq'},
        {value: 1548, name: 'bilibili'},
        {value: 335, name: 'baidu1'},
        {value: 310, name: 'neteasy1'},
        {value: 234, name: 'iqiyi1'},
        {value: 135, name: 'qq1'},
        {value: 1548, name: 'bilibili1'}
      ],
      protocol_label: ['HTTP', 'DNS', 'SSL', 'DHCP', 'Unknow','HTTP1', 'DNS1', 'SSL1', 'DHCP1', 'Unknow1'],
      protocol_data: [
        {value: 335, name: 'HTTP'},
        {value: 310, name: 'DNS'},
        {value: 234, name: 'DHCP'},
        {value: 135, name: 'Unknow'},
        {value: 1548, name: 'SSL'},
        {value: 335, name: 'HTTP1'},
        {value: 310, name: 'DNS1'},
        {value: 234, name: 'DHCP1'},
        {value: 135, name: 'Unknow1'},
        {value: 1548, name: 'SSL1'}],
        data1:[
          {
            srcmac: "34:23:87:A9:26:9B",
            desmac: "D4:EE:07:32:01:5A",
            srcip: "192.168.199.162",
            desip: "119.3.227.169",
            srcport: "17600",
            desport: "47873",
            address: "NULL",
            date: "2019-06-19 23:13:52",
            protocol: "DNS",
            byte: "6956",
            dangerous: true
          },
          {
            srcmac: "34:23:87:A9:26:9B",
            desmac: "D4:EE:07:32:01:5B",
            srcip: "192.168.199.162",
            desip: "119.3.227.168",
            srcport: "17600",
            desport: "47875",
            address: "NULL",
            date: "2019-06-19 23:13:43",
            protocol: "UDP",
            byte: "6956",
            dangerous: false
          },
          {
            srcmac: "34:23:87:A9:26:9B",
            desmac: "D4:EE:07:32:01:50",
            srcip: "192.168.199.162",
            desip: "119.3.227.166",
            srcport: "17600",
            desport: "47870",
            address: "NULL",
            date: "2019-06-19 23:13:52",
            protocol: "HTTP",
            byte: "6956",
            dangerous: true
          },
          {
            srcmac: "34:23:87:A9:26:9B",
            desmac: "D4:EE:07:32:01:5B",
            srcip: "192.168.199.162",
            desip: "119.3.227.120",
            srcport: "17600",
            desport: "47875",
            address: "NULL",
            date: "2019-06-19 23:13:53",
            protocol: "SSL",
            byte: "6956",
            dangerous: false
          },
        ],
*/
      columns1: [
        {
          title: '目的MAC地址',
          key: 'desmac',
          sortable:true,
          tooltip:true
        },
        {
          title: '目的IP地址',
          key: 'desip',
          sortable:true,
          tooltip:true
        },
        {
          title: '目的端口地址',
          key: 'desport',
          sortable:true,
          tooltip:true
        },
        {
          title: '协议',
          key: 'protocol',
          sortable:true,
          tooltip:true
        },
        {
          title: '网址',
          key: 'address',
          sorttable:true,
          render:(h,params)=>{
            if (params.row.dangerous == 'true'){
              return h('span',{style:{color:'red'},},params.row.address);
            }else{
              return h('span',params.row.address);
            }
          },
          filters:[
            {
              label:'危险网址',
              value: 1
            }
          ],
          filterMultiple:false,
          filterMethod(value,row){
            if(value == 1){
              return row.dangerous == 'true';
            }
          }
        },
        {
          title: '字节',
          key: 'byte',
          sortable:true,
          tooltip:true
        },
        {
          title: '日期',
          key: 'date',
          sortable:true,
          tooltip:true
        }
        ],

      charts: '',
      myChart: '',
      portdata_x: '',
      portdata_y: '',
      desdata_x: '',
      desdata_y: '',
      ip_data: [],
      ap_data1: [],
      //website_label: '',
      //website_data: '',
      protocol_label: '',
      protocol_data: '',
      data1:[],
      ap_data:'',

      modal1: false,
    }
   },
  methods: {
    getdata: function(Ip,Mac,start_date,stop_date){
      let s = this
      this.$axios.get('getinfo',{
        params:{
          ip: Ip,
          mac :Mac,
          ap_mac:this.ap_mac,
          start_date: start_date,
          stop_date : stop_date,
          page_id : 0
        }
      })
      .then(function(response){
        s.protocol_label = response.data['protocol_label'];
        s.protocol_data = response.data['protocol_data'];
        s.desdata_x = response.data['desdata_x'];
        s.desdata_y = response.data['desdata_y'];
        s.portdata_x = response.data['portdata_x'];
        s.portdata_y = response.data['portdata_y'];
        s.ip_data = response.data['ip_data'];
        s.ap_data1 = response.data['ap_data1'];
        s.count = response.data['count'];
        s.data1 = response.data['ipinfo'];
        //s.website_label = response.data['website_label'];
        //s.website_data = response.data['website_data'];
        //s.data1 = response.data['ipinfo'];
        //s.ap_data = response.data['ap_data'];
        //alert(response.data['ipinfo'][0]['srcmac']);
        //alert(response.data['ap_data'][0]['name']);
        s.drawDes();
        s.drawport();
        s.draw_protocol('protocol');
        //s.draw_website('website');
        //s.draw_protocol('protocol');
        //s.initEchart('container');
      });
    },
    draw_website: function(id){
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
        title: {
          text:'网址统计',
          subtext: '',
          x:'center',
          textStyle:{
            color:"#222",
            fontStyle:"normal",
            fontWeight:"600",
            fontFamily:"san-serif",
            fontSize:16,
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a}<br/>{b}:{c} ({d}%)'
        },
        legend: {
          type: 'scroll',
          orient: 'vertical',
          right:0,
          data:this.website_label,
        },
        series: [
          {
          name:'网址统计',
          type:'pie',
          radius:['30%','50%'],
          avoidLabelOverlap: false,
          label: {
            normal: {
              show: false,
              position: 'center'
            },
            emphasis: {
              show: true,
              textStyle: {
                fontSize: '30',
                fontWeight: 'blod'
              }
            }
          },
          labelLine: {
            normal: {
              show: false
            }
          },
          data:this.website_data

          }
        ]
      })
    },
    draw_protocol: function(id){
      this.charts = echarts.init(document.getElementById(id))
      this.charts.setOption({
        title: {
          text:'协议分布',
          subtext: '',
          x:'center',
          textStyle:{
            color:"#222",
            fontStyle:"normal",
            fontWeight:"600",
            fontFamily:"san-serif",
            fontSize:16,
          }
        },
        tooltip: {
          trigger: 'item',
          formatter: '{a}<br/>{b}:{c} ({d}%)'
        },
        legend: {
          orient: 'vertical',
          right:0,
          data:this.protocol_label,
        },
        series: [
          {
          name:'协议分布',
          type:'pie',
          radius:['30%','50%'],
          avoidLabelOverlap: false,
          label: {
            normal: {
              show: false,
              position: 'center'
            },
            emphasis: {
              show: true,
              textStyle: {
                fontSize: '30',
                fontWeight: 'blod'
              }
            }
          },
          labelLine: {
            normal: {
              show: false
            }
          },
          data:this.protocol_data

          }
        ]
      })
    },
    initEchart(id) {
      this.myChart = echarts.init(document.getElementById(id));
      this.myChart.setOption({
        /*
        title: {
          text:'连接关系',
          subtext: '红色为AP\n蓝色为STA\n绿色为选中的AP',
          subtextStyle:{
            color:"#222",
          },
          left: 20,
          x:'center',
          textStyle:{
            color:"#222",
            fontStyle:"normal",
            fontWeight:"600",
            fontFamily:"san-serif",
            fontSize:16,
          }
        },*/
        tooltip: {
          trigger: 'item',
          formatter: '{b}<br/>{c}'
        },
        series:[{
          type: 'tree',
          data: this.ap_data,
          top: '1%',
          left: '7%',
          bottom: '1%',
          right: '20%',
          symbolSize: 7,
          label: {
            normal: {
              position: 'top',
              verticalAlign: 'middle',
              align: 'left',
              fontSize: 15,
              color: 'red',
            }
          },

          leaves: {
            label: {
              normal: {
                position: 'top',
                verticalAlign: 'middle',
                align: 'middle',
                color: 'blue'
              }
            }
          },
          expandAndCollapse: false,
          animationDuration: 550,
          animationDurationUpdate: 750
            }]
      })
    },
    help :function(){
      this.modal1 = true
    },
    choose_layer: function(name){
      if(name == 'network'){
        this.drawDes();
      }
      else if(name == 'transport'){
        //alert(1)
        this.drawDes();
      }
      else if (name == 'application') {
        this.draw_protocol('protocol');
        //this.draw_website('website');
      }
    },
    drawDes: function() {
      this.chart = echarts.init(this.$refs.desEchart);
      // 把配置和数据放这里
      this.chart.setOption({
        color: ['#3398DB'],
        title: {
          text:'服务器IP流量',
          subtext: '',
          x:'center',
          textStyle:{
            color:"#222",
            fontStyle:"normal",
            fontWeight:"600",
            fontFamily:"san-serif",
            fontSize:16,
            lineHeight:50,
          }
        },

        tooltip: {
          trigger: 'axis',
          axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'line' // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        yAxis: [{
          type: 'category',
          data: this.desdata_y,
          axisTick: {
            alignWithLabel: true
          }
        }],
        xAxis: [{
          type: 'value'
        }],
        series: [{
          name: '服务器IP流量',
          type: 'bar',
          barWidth: '60%',
          data: this.desdata_x,
        }]
      })

    },
    drawport: function() {
      this.chart = echarts.init(this.$refs.portEchart);
      // 把配置和数据放这里
      this.chart.setOption({
        color: ['#3398DB'],
        title: {
          text:'端口统计',
          subtext: '',
          x:'center',
          textStyle:{
            color:"#222",
            fontStyle:"normal",
            fontWeight:"600",
            fontFamily:"san-serif",
            fontSize:16,
            lineHeight:50,
          }
        },

        tooltip: {
          trigger: 'axis',
          axisPointer: { // 坐标轴指示器，坐标轴触发有效
            type: 'line' // 默认为直线，可选为：'line' | 'shadow'
          }
        },
        grid: {
          left: '3%',
          right: '4%',
          bottom: '3%',
          containLabel: true
        },
        yAxis: [{
          type: 'category',
          data: this.portdata_y,
          axisTick: {
            alignWithLabel: true
          }
        }],
        xAxis: [{
          type: 'value'
        }],
        series: [{
          name: '端口统计',
          type: 'bar',
          barWidth: '60%',
          data: this.portdata_x,
        }]
      })
    },
    change_page :function(index){
      let s = this
      this.$axios.get('getflow',{
        params:{
          ip: this.$route.query.ip,
          mac: this.$route.query.mac,
          ap_mac:this.ap_mac,
          start_date: this.start_date,
          stop_date : this.stop_date,
          page_id : index-1,
        }
      })
      .then(function(response){
        s.data1 = response.data['ipinfo'];
      });
    },
    handleClick () {
      this.open = true;
    },
    handleChange (date) {

    },
    handleClear () {
        this.open = false;
        this.visible=false;
    },
    handleOk () {
        this.showdate = this.datechange(this.dates[0])+"-"+this.datechange(this.dates[1]);
        this.date_route(this.datechange(this.dates[0]).replace('/','-').replace('/','-'),this.datechange(this.dates[1]).replace('/','-').replace('/','-'))
        this.open = false;
        this.visible = false;
        this.start_date = start_date;
        this.stop_date = stop_date;
    },
    dropopen (){
      this.visible=true;
    },

    getDay(day){
      var today = new Date();
      var targetday_milliseconds=today.getTime() + 1000*60*60*24*day;
      today.setTime(targetday_milliseconds); //注意，这行是关键代码
      var tYear = today.getFullYear();
      var tMonth = today.getMonth();
      var tDate = today.getDate();
      tMonth = this.doHandleMonth(tMonth + 1);
      tDate =  this.doHandleMonth(tDate);
      return tYear+"-"+tMonth+"-"+tDate;
    },
    doHandleMonth(month){
      var m = month;
      if(month.toString().length == 1){
        m = "0" + month;
      }
      return m;
    },
    datechoose:function(name){
      if(name=='1'){

        var start_date=this.getDay(-6);
        var stop_date=this.getDay(0);
        this.date_route(start_date,stop_date);
        //alert(start_date+" "+stop_date);
        this.showdate = '一周';
        this.visible=false;
        this.start_date = start_date;
        this.stop_date = stop_date;
      }
      else if (name=='2') {
        var start_date=this.getDay(-30);
        var stop_date=this.getDay(0);
        this.date_route(start_date,stop_date);
        this.showdate = '一个月';
        this.visible=false;
        this.start_date = start_date;
        this.stop_date = stop_date;
      }
      else if (name=='3') {
        var start_date=this.getDay(-91);
        var stop_date=this.getDay(0);
        this.date_route(start_date,stop_date);
        this.showdate = '三个月';
        this.visible=false;
        this.start_date = start_date;
        this.stop_date = stop_date;
      }
      else if (name=='4') {
        var start_date=this.getDay(-182);
        var stop_date=this.getDay(0);
        this.date_route(start_date,stop_date);
        this.showdate = '六个月';
        this.visible=false;
        this.start_date = start_date;
        this.stop_date = stop_date;
      }
      else if (name=='5') {
        var start_date=this.getDay(-365);
        var stop_date=this.getDay(0);
        this.date_route(start_date,stop_date);
        this.showdate = '一年';
        this.visible=false;
        this.start_date = start_date;
        this.stop_date = stop_date;
      }
      else if (name=='6') {

      }
    },
    date_route: function(start_date,stop_date){
      this.$router.push({
        path: '/parserinfo',
        query:{
          ip : this.$route.query.ip,
          mac: this.$route.query.mac,
          ap: this.ap_mac,
          start_date:start_date,
          stop_date: stop_date,
          page_id : 0,
        }
      })
    },
    datechange: function(date){
        var month = date.getMonth()+1;
        var year = date.getFullYear();
        var day = date.getDate();
        var d = year+"/"+month+"/"+day;
        return d;
    },
    choose_proto: function(value){
      alert(value)
    },
    choose_ap: function(){
      this.modal1=true
    },
    reload () {
      this.isRouterAlive = false
      this.$nextTick(() => (this.isRouterAlive = true))
    }
  }
}
</script>
