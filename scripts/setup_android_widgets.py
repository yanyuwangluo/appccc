from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ANDROID_MAIN = ROOT / "mobile_template" / "android" / "app" / "src" / "main"
MANIFEST_PATH = ANDROID_MAIN / "AndroidManifest.xml"
RES_XML = ANDROID_MAIN / "res" / "xml"
RES_LAYOUT = ANDROID_MAIN / "res" / "layout"
RES_VALUES = ANDROID_MAIN / "res" / "values"

PACKAGE_NAME = "com.example.mobile_template"


def ensure_dirs() -> None:
    RES_XML.mkdir(parents=True, exist_ok=True)
    RES_LAYOUT.mkdir(parents=True, exist_ok=True)
    RES_VALUES.mkdir(parents=True, exist_ok=True)
    kotlin_dir = ANDROID_MAIN / "kotlin" / Path(*PACKAGE_NAME.split("."))
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
    android:padding="10dp"
    android:orientation="vertical"
    android:background="@android:color/white">

    <TextView
        android:id="@+id/widget_title"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="青岛天气"
        android:textStyle="bold"
        android:textSize="14sp"
        android:textColor="@android:color/black" />

    <TextView
        android:id="@+id/widget_value"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="6dp"
        android:maxLines="2"
        android:ellipsize="end"
        android:text="点击 App 刷新天气"
        android:textSize="12sp"
        android:textColor="@android:color/black" />
</LinearLayout>
""",
        encoding="utf-8",
    )

    (RES_LAYOUT / "dashboard_widget_large_layout.xml").write_text(
        """<?xml version="1.0" encoding="utf-8"?>
<LinearLayout xmlns:android="http://schemas.android.com/apk/res/android"
    android:layout_width="match_parent"
    android:layout_height="match_parent"
    android:padding="12dp"
    android:orientation="vertical"
    android:background="@android:color/white">

    <TextView
        android:id="@+id/widget_title"
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:text="青岛天气"
        android:textStyle="bold"
        android:textSize="16sp"
        android:textColor="@android:color/black" />

    <TextView
        android:id="@+id/widget_value"
        android:layout_width="match_parent"
        android:layout_height="wrap_content"
        android:layout_marginTop="8dp"
        android:maxLines="6"
        android:ellipsize="end"
        android:text="点击 App 刷新天气"
        android:textSize="13sp"
        android:textColor="@android:color/black" />
</LinearLayout>
""",
        encoding="utf-8",
    )


def write_provider() -> None:
    kotlin_dir = ANDROID_MAIN / "kotlin" / Path(*PACKAGE_NAME.split("."))
    (kotlin_dir / "DashboardWidgetProvider.kt").write_text(
        f"""package {PACKAGE_NAME}

import android.appwidget.AppWidgetManager
import android.appwidget.AppWidgetProvider
import android.content.Context
import android.widget.RemoteViews

class DashboardWidgetProviderSmall : AppWidgetProvider() {{
    override fun onUpdate(context: Context, appWidgetManager: AppWidgetManager, appWidgetIds: IntArray) {{
        updateAll(context, appWidgetManager, appWidgetIds, R.layout.dashboard_widget_small_layout)
    }}
}}

class DashboardWidgetProviderLarge : AppWidgetProvider() {{
    override fun onUpdate(context: Context, appWidgetManager: AppWidgetManager, appWidgetIds: IntArray) {{
        updateAll(context, appWidgetManager, appWidgetIds, R.layout.dashboard_widget_large_layout)
    }}
}}

private fun updateAll(
    context: Context,
    appWidgetManager: AppWidgetManager,
    appWidgetIds: IntArray,
    layoutId: Int,
) {{
    val sp = context.getSharedPreferences("HomeWidgetPreferences", Context.MODE_PRIVATE)
    val title = sp.getString("widget_title", "青岛天气") ?: "青岛天气"
    val value = sp.getString("widget_value", "点击 App 刷新天气") ?: "点击 App 刷新天气"

    appWidgetIds.forEach {{ widgetId ->
        val views = RemoteViews(context.packageName, layoutId)
        views.setTextViewText(R.id.widget_title, title)
        views.setTextViewText(R.id.widget_value, value)
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
    text = text.replace(
        "<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\">",
        "<manifest xmlns:android=\"http://schemas.android.com/apk/res/android\">\\n    <uses-permission android:name=\"android.permission.INTERNET\"/>",
    )

    small_receiver = """
        <receiver
            android:name=".DashboardWidgetProviderSmall"
            android:exported="false">
            <intent-filter>
                <action android:name="android.appwidget.action.APPWIDGET_UPDATE" />
            </intent-filter>
            <meta-data
                android:name="android.appwidget.provider"
                android:resource="@xml/dashboard_widget_small_info" />
        </receiver>
"""
    large_receiver = """
        <receiver
            android:name=".DashboardWidgetProviderLarge"
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
