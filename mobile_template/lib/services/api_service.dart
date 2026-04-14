import "package:dio/dio.dart";

class DashboardData {
  final String title;
  final String value;
  final String subtitle;
  final String link;
  final DateTime updatedAt;

  const DashboardData({
    required this.title,
    required this.value,
    required this.subtitle,
    required this.link,
    required this.updatedAt,
  });
}

class ApiService {
  static const String baseUrl = "https://api.suol.cc";
  final Dio _dio = Dio(
    BaseOptions(
      baseUrl: baseUrl,
      connectTimeout: const Duration(seconds: 10),
      receiveTimeout: const Duration(seconds: 10),
    ),
  );

  Future<DashboardData> fetchLatestData() async {
    try {
      return await _fetchFromRemote();
    } on DioException catch (_) {
      // Network on mobile can be unstable on first request; retry once.
      return _fetchFromRemote();
    }
  }

  Future<DashboardData> _fetchFromRemote() async {
    final Response<dynamic> response = await _dio.get("/v1/update_cartoon.php");
    final dynamic raw = response.data;
    if (raw is! Map<String, dynamic>) {
      throw Exception("动漫接口返回格式异常");
    }

    if (raw["code"] != 200) {
      throw Exception("动漫接口返回失败: ${raw["code"]}");
    }

    final dynamic list = raw["data"];
    if (list is! List || list.isEmpty) {
      throw Exception("动漫接口暂无更新数据");
    }

    final dynamic first = list.first;
    if (first is! Map<String, dynamic>) {
      throw Exception("动漫接口数据项格式异常");
    }

    final String today = raw["today"]?.toString() ?? "";
    final String week = raw["today_week"]?.toString() ?? "";
    final String type = first["type"]?.toString() ?? first["类型"]?.toString() ?? "动漫";
    final String desc = first["desc"]?.toString() ?? "暂无简介";
    final String upTime = first["up_time"]?.toString() ?? "--:--";
    final String upDate = first["up_date"]?.toString() ?? first["update_date"]?.toString() ?? "更新信息未知";
    final String title = first["title"]?.toString() ?? first["标题"]?.toString() ?? "未知作品";
    final String link = first["link"]?.toString() ?? first["链接"]?.toString() ?? "";
    final String subtitle = "更新 $upTime | $upDate | $type";

    return DashboardData(
      title: "$title${today.isNotEmpty || week.isNotEmpty ? " ($today $week)" : ""}",
      value: desc,
      subtitle: subtitle,
      link: link,
      updatedAt: DateTime.now(),
    );
  }
}
