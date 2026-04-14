import "package:home_widget/home_widget.dart";

import "../services/api_service.dart";

class WidgetSyncService {
  static const String androidWidgetNameSmall = "DashboardWidgetProviderSmall";
  static const String androidWidgetNameLarge = "DashboardWidgetProviderLarge";
  static const String iOSWidgetName = "DashboardWidget";

  final ApiService _apiService;

  WidgetSyncService(this._apiService);

  Future<DashboardData> refreshWidgetData() async {
    final DashboardData data = await _apiService.fetchLatestData();

    await HomeWidget.saveWidgetData<String>("widget_title", data.title);
    await HomeWidget.saveWidgetData<String>("widget_value", data.value);
    await HomeWidget.saveWidgetData<String>("widget_updated", data.updatedAt.toIso8601String());

    await HomeWidget.updateWidget(
      androidName: androidWidgetNameSmall,
      iOSName: iOSWidgetName,
    );

    await HomeWidget.updateWidget(
      androidName: androidWidgetNameLarge,
      iOSName: iOSWidgetName,
    );

    return data;
  }
}
