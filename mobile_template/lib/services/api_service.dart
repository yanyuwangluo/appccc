import "package:dio/dio.dart";

class DashboardData {
  final String title;
  final String value;
  final DateTime updatedAt;

  const DashboardData({
    required this.title,
    required this.value,
    required this.updatedAt,
  });
}

class ApiService {
  static const String baseUrl = "https://api.suol.cc";
  final Dio _dio = Dio(BaseOptions(baseUrl: baseUrl, connectTimeout: const Duration(seconds: 8)));

  Future<DashboardData> fetchLatestData() async {
    final Response<dynamic> response = await _dio.get(
      "/v1/tq_tips.php",
      queryParameters: <String, dynamic>{
        "type": "today",
        "msg": "青岛",
        "n": 1,
      },
    );
    final dynamic raw = response.data;
    if (raw is! Map<String, dynamic>) {
      throw Exception("天气接口返回格式异常");
    }

    if (raw["code"] != 200) {
      throw Exception("天气接口返回失败: ${raw["code"]}");
    }

    final dynamic data = raw["data"];
    final String weather = (data is Map<String, dynamic>) ? (data["weather"]?.toString() ?? "暂无天气数据") : "暂无天气数据";

    return DashboardData(
      title: "青岛天气",
      value: weather,
      updatedAt: DateTime.now(),
    );
  }
}
