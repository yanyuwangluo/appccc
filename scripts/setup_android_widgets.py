import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANDROID_MAIN = ROOT / "mobile_template" / "android" / "app" / "src" / "main"
MANIFEST_PATH = ANDROID_MAIN / "AndroidManifest.xml"
APP_GRADLE_KTS = ROOT / "mobile_template" / "android" / "app" / "build.gradle.kts"
APP_GRADLE = ROOT / "mobile_template" / "android" / "app" / "build.gradle"
RES_XML = ANDROID_MAIN / "res" / "xml"
RES_LAYOUT = ANDROID_MAIN / "res" / "layout"
RES_VALUES = ANDROID_MAIN / "res" / "values"

PACKAGE_NAME = "com.example.mobile_template"


def detect_package_name() -> str:
    candidates = [APP_GRADLE_KTS, APP_GRADLE]
    pattern = re.compile(r'namespace\s*=\s*"([^"]+)"')
    for file in candidates:
        if not file.exists():
            continue
        text = file.read_text(encoding="utf-8")
        match = pattern.search(text)
        if match:
            return match.group(1).strip()
    return PACKAGE_NAME


def ensure_dirs() -> None:
    package_name = detect_package_name()
    RES_XML.mkdir(parents=True, exist_ok=True)
    RES_LAYOUT.mkdir(parents=True, exist_ok=True)
    RES_VALUES.mkdir(parents=True, exist_ok=True)
    kotlin_dir = ANDROID_MAIN / "kotlin" / Path(*package_name.split("."))
    kotlin_dir.mkdir(parents=True, exist_ok=True)


def write_widget_xml() -> None:
    (RES_XML / "dashboard_widget_small_info.xml").write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:description="@string/widget_desc_small"
    android:minWidth="110dp"
    android:minHeight="40dp"
    android:updatePeriodMillis="0"
    android:initialLayout="@layout/dashboard_widget_small_layout"
    android:resizeMode="horizontal|vertical"
    android:widgetCategory="home_screen" />
""",
        encoding="utf-8",
    )

    (RES_XML / "dashboard_widget_large_info.xml").write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<appwidget-provider xmlns:android="http://schemas.android.com/apk/res/android"
    android:description="@string/widget_desc_large"
    android:minWidth="250dp"
    android:minHeight="110dp"
    android:updatePeriodMillis="0"
    android:initialLayout="@layout/dashboard_widget_large_layout"
    android:resizeMode="horizontal|vertical"
    android:widgetCategory="home_screen" />
""",
        encoding="utf-8",
    )

    (RES_VALUES / "home_widget_strings.xml").write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="widget_desc_small">Weather widget small</string>
    <string name="widget_desc_large">Weather widget large</string>
</resources>
""",
        encoding="utf-8",
    )


def write_widget_layouts() -> None:
    (RES_LAYOUT / "dashboard_widget_small_layout.xml").write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="12dp"
    android:orientation="vertical"
    android:background="#111827">

    <TextView
        android:id="@+id/widget_title"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="今日动漫更新"
        android:textStyle="bold"
        android:textSize="14sp"
        android:textColor="#F9FAFB" />

    <TextView
        android:id="@+id/widget_value"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="6dp"
        android:maxLines="2"
        android:ellipsize="end"
        android:text="打开 App 拉取最新动漫更新"
        android:textSize="12sp"
        android:textColor="#E5E7EB" />

    <TextView
        android:id="@+id/widget_subtitle"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="6dp"
        android:maxLines="1"
        android:ellipsize="end"
        android:text="更新时间 --:--"
        android:textSize="10sp"
        android:textColor="#93C5FD" />
</LinearLayout>
""",
        encoding="utf-8",
    )

    (RES_LAYOUT / "dashboard_widget_large_layout.xml").write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="14dp"
    android:orientation="vertical"
    android:background="#0B1220">

    <TextView
        android:id="@+id/widget_title"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="今日动漫更新"
        android:textStyle="bold"
        android:textSize="17sp"
        android:textColor="#FFFFFF" />

    <TextView
        android:id="@+id/widget_value"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:maxLines="4"
        android:ellipsize="end"
        android:text="打开 App 拉取最新动漫更新"
        android:textSize="13sp"
        android:textColor="#E2E8F0" />

    <TextView
        android:id="@+id/widget_subtitle"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="10dp"
        android:maxLines="2"
        android:ellipsize="end"
        android:text="更新时间 --:--"
        android:textSize="11sp"
        android:textColor="#93C5FD" />
</LinearLayout>
""",
        encoding="utf-8",
    )


def write_provider() -> None:
    package_name = detect_package_name()
    kotlin_root = ANDROID_MAIN / "kotlin"
    kotlin_dir = kotlin_root / Path(*package_name.split("."))
    for old in kotlin_root.rglob("DashboardWidgetProvider.kt"):
        if old.parent != kotlin_dir:
            old.unlink()

    (kotlin_dir / "DashboardWidgetProvider.kt").write_text(
        f"""package {package_name}

import android.appwidget.AppWidgetManager
import android.content.Context
import android.content.SharedPreferences
import android.widget.RemoteViews
import es.antonborri.home_widget.HomeWidgetProvider

class DashboardWidgetProviderSmall : HomeWidgetProvider() {{
    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray,
        widgetData: SharedPreferences,
    ) {{
        updateAll(context, appWidgetManager, appWidgetIds, widgetData, R.layout.dashboard_widget_small_layout)
    }}
}}

class DashboardWidgetProviderLarge : HomeWidgetProvider() {{
    override fun onUpdate(
        context: Context,
        appWidgetManager: AppWidgetManager,
        appWidgetIds: IntArray,
        widgetData: SharedPreferences,
    ) {{
        updateAll(context, appWidgetManager, appWidgetIds, widgetData, R.layout.dashboard_widget_large_layout)
    }}
}}

private fun updateAll(
    context: Context,
    appWidgetManager: AppWidgetManager,
    appWidgetIds: IntArray,
    widgetData: SharedPreferences,
    layoutId: Int,
) {{
    val title = widgetData.getString("widget_title", "今日动漫更新") ?: "今日动漫更新"
    val value = widgetData.getString("widget_value", "打开 App 拉取最新动漫更新") ?: "打开 App 拉取最新动漫更新"
    val subtitle = widgetData.getString("widget_subtitle", "更新时间 --:--") ?: "更新时间 --:--"

    appWidgetIds.forEach {{ widgetId ->
        val views = RemoteViews(context.packageName, layoutId)
        views.setTextViewText(R.id.widget_title, title)
        views.setTextViewText(R.id.widget_value, value)
        views.setTextViewText(R.id.widget_subtitle, subtitle)
        appWidgetManager.updateAppWidget(widgetId, views)
    }}
}}
""",
        encoding="utf-8",
    )


def patch_manifest() -> None:
    if not MANIFEST_PATH.exists():
        raise FileNotFoundError(f"AndroidManifest not found: {{MANIFEST_PATH}}")

    text = MANIFEST_PATH.read_text(encoding="utf-8")
    if 'android.permission.INTERNET' not in text:
        text = re.sub(
            r"(<manifest\b[^>]*>)",
            r'\1\n    <uses-permission android:name="android.permission.INTERNET"/>',
            text,
            count=1,
        )

    package_name = detect_package_name()
    small_receiver = f"""
        <receiver
            android:name="{package_name}.DashboardWidgetProviderSmall"
            android:exported="false">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
            </intent-filter>
            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/dashboard_widget_small_info" />
        </receiver>
"""
    large_receiver = f"""
        <receiver
            android:name="{package_name}.DashboardWidgetProviderLarge"
            android:exported="false">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
            </intent-filter>
            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/dashboard_widget_large_info" />
        </receiver>
"""

    if "DashboardWidgetProviderSmall" not in text:
        text = text.replace("</application>", f"{small_receiver}\\n{large_receiver}\\n    </application>")

    MANIFEST_PATH.write_text(text, encoding="utf-8")


def main() -> None:
    ensure_dirs()
    write_widget_xml()
    write_widget_layouts()
    write_provider()
    patch_manifest()
    print("Android widget files generated.")


if __name__ == "__main__":
    main()
