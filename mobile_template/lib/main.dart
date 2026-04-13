import "package:flutter/material.dart";
import "package:home_widget/home_widget.dart";

import "services/api_service.dart";
import "widget/widget_sync_service.dart";

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: "天气小组件",
      theme: ThemeData(colorScheme: ColorScheme.fromSeed(seedColor: Colors.blue), useMaterial3: true),
      home: const HomePage(),
    );
  }
}

class HomePage extends StatefulWidget {
  const HomePage({super.key});

  @override
  State<HomePage> createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  final WidgetSyncService _syncService = WidgetSyncService(ApiService());
  String _title = "未刷新";
  String _value = "--";
  String _status = "点击按钮拉取天气并刷新小组件";

  Future<void> _refresh() async {
    setState(() {
      _status = "刷新中...";
    });

    try {
      final DashboardData data = await _syncService.refreshWidgetData();
      if (!mounted) return;
      setState(() {
        _title = data.title;
        _value = data.value;
        _status = "刷新成功: ${data.updatedAt}";
      });
    } catch (e) {
      if (!mounted) return;
      setState(() {
        _status = "刷新失败: $e";
      });
    }
  }

  Future<String?> _pickWidgetStyle() async {
    return showModalBottomSheet<String>(
      context: context,
      builder: (BuildContext context) {
        return SafeArea(
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: <Widget>[
              ListTile(
                title: const Text("2x1 小号组件"),
                onTap: () => Navigator.of(context).pop("small"),
              ),
              ListTile(
                title: const Text("4x2 大号组件"),
                onTap: () => Navigator.of(context).pop("large"),
              ),
            ],
          ),
        );
      },
    );
  }

  Future<void> _pinWidget() async {
    try {
      final bool supported = await HomeWidget.isRequestPinWidgetSupported();
      if (!supported) {
        if (!mounted) return;
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text("当前设备不支持应用内直接添加小组件，请手动到桌面添加。")),
        );
        return;
      }

      final String? style = await _pickWidgetStyle();
      if (style == null) {
        return;
      }

      final String widgetName = style == "large"
          ? WidgetSyncService.androidWidgetNameLarge
          : WidgetSyncService.androidWidgetNameSmall;

      await HomeWidget.requestPinWidget(
        name: widgetName,
      );

      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("已发起添加${style == "large" ? "4x2" : "2x1"}小组件请求，请在系统弹窗中确认。")),
      );
    } catch (e) {
      if (!mounted) return;
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text("发起添加小组件失败: $e")),
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text("天气接口 + 小组件")),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Text("城市: $_title", style: Theme.of(context).textTheme.titleLarge),
            const SizedBox(height: 8),
            Text("天气: $_value", style: Theme.of(context).textTheme.titleMedium),
            const SizedBox(height: 16),
            Text(_status),
            const SizedBox(height: 24),
            FilledButton(
              onPressed: _refresh,
              child: const Text("拉取天气并刷新小组件"),
            ),
            const SizedBox(height: 12),
            OutlinedButton(
              onPressed: _pinWidget,
              child: const Text("添加到桌面小组件"),
            ),
          ],
        ),
      ),
    );
  }
}
