import { useState, useEffect } from 'react';
import axios from 'axios';
import { Layout, Menu } from 'antd';
import EChartsReact from 'echarts-for-react';
import "antd/dist/reset.css";

const { Sider, Content } = Layout;

function App() {
  const [activeKey, setActiveKey] = useState("year");
  const [chartData, setChartData] = useState([]);

  // 切换菜单自动请求对应图表数据
  useEffect(() => {
    const fetchData = async () => {
      let url = "";
      switch(activeKey) {
        case "year":
          url = "http://127.0.0.1:5000/api/chart/year_count";
          break;
        case "region":
          url = "http://127.0.0.1:5000/api/chart/region_count";
          break;
        case "type":
          url = "http://127.0.0.1:5000/api/chart/type_count";
          break;
        case "score":
          url = "http://127.0.0.1:5000/api/chart/score_vote";
          break;
        default:
          return;
      }
      const res = await axios.get(url);
      setChartData(res.data.data);
    };
    fetchData();
  }, [activeKey])

  // 根据菜单渲染对应图表配置
  const getOption = () => {
    switch(activeKey) {
      case "year":
        return {
          title: { text: "各年份电影数量分布" },
          xAxis: { type: "category", data: chartData.map(item => item.year) },
          yAxis: { type: "value" },
          series: [{ type: "bar", data: chartData.map(item => item.count) }]
        }
      case "region":
        return {
          title: { text: "各制片地区电影数量" },
          xAxis: { type: "category", data: chartData.map(item => item.name) },
          yAxis: { type: "value" },
          series: [{ type: "bar", data: chartData.map(item => item.value) }]
        }
      case "type":
        return {
          title: { text: "影片类型占比" },
          series: [{ type: "pie", radius: "50%", data: chartData }]
        }
      case "score":
        return {
          title: { text: "评分-评价人数热度散点图" },
          xAxis: { type: "value", name: "评分" },
          yAxis: { type: "value", name: "评价人数" },
          series: [{ type: "scatter", data: chartData.map(item => [item.score, item.vote, item.name]) }]
        }
      default:
        return {}
    }
  }

  return (
    <Layout style={{ minHeight: "100vh" }}>
      {/* Ant Design 侧边菜单 */}
      <Sider width={200}>
        <Menu
          mode="vertical"
          selectedKeys={[activeKey]}
          onClick={({key}) => setActiveKey(key)}
          style={{ height: "100%" }}
        >
          <Menu.Item key="year">年份统计柱状图</Menu.Item>
          <Menu.Item key="region">地区统计柱状图</Menu.Item>
          <Menu.Item key="type">影片类型饼图</Menu.Item>
          <Menu.Item key="score">评分热度散点图</Menu.Item>
        </Menu>
      </Sider>
      <Content style={{ padding: "30px" }}>
        <EChartsReact option={getOption()} style={{ width:"100%", height:"600px" }} />
      </Content>
    </Layout>
  );
}

export default App;