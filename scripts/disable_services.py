#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
sys.path.insert(0, str(SRC))

from zed_cn_macos.config import load_paths


def replace_exact(path: Path, old: str, new: str) -> None:
    content = path.read_text()
    if old not in content:
        raise RuntimeError(f"Expected snippet not found in {path}")
    path.write_text(content.replace(old, new, 1))


def main() -> int:
    paths = load_paths(ROOT)
    main_rs = paths.source_dir / "crates" / "zed" / "src" / "main.rs"
    zed_rs = paths.source_dir / "crates" / "zed" / "src" / "zed.rs"

    replace_exact(
        main_rs,
        """        let telemetry = client.telemetry();
        telemetry.start(
            system_id.as_ref().map(|id| id.to_string()),
            installation_id.as_ref().map(|id| id.to_string()),
            session.id().to_owned(),
            cx,
        );
        cx.subscribe(&user_store, {
            let telemetry = telemetry.clone();
            move |_, evt: &client::user::Event, _| match evt {
                client::user::Event::PrivateUserInfoUpdated => {
                    crashes::set_user_info(crashes::UserInfo {
                        metrics_id: telemetry.metrics_id().map(|s| s.to_string()),
                        is_staff: telemetry.is_staff(),
                    });
                }
                _ => {}
            }
        })
        .detach();

        // We should rename these in the future to `first app open`, `first app open for release channel`, and `app open`
        if let (Some(system_id), Some(installation_id)) = (&system_id, &installation_id) {
            match (&system_id, &installation_id) {
                (IdType::New(_), IdType::New(_)) => {
                    telemetry::event!("App First Opened");
                    telemetry::event!("App First Opened For Release Channel");
                }
                (IdType::Existing(_), IdType::New(_)) => {
                    telemetry::event!("App First Opened For Release Channel");
                }
                (_, IdType::Existing(_)) => {
                    telemetry::event!("App Opened");
                }
            }
        }
""",
        """        // Eqavo disables upstream telemetry startup and app-open event reporting.
""",
    )

    replace_exact(
        main_rs,
        """        auto_update::init(client.clone(), cx);
        dap_adapters::init(cx);
        auto_update_ui::init(cx);
""",
        """        // Eqavo disables upstream auto update initialization.
        dap_adapters::init(cx);
""",
    )

    replace_exact(
        main_rs,
        """        channel::init(&app_state.client.clone(), app_state.user_store.clone(), cx);
""",
        """        // Eqavo disables collaboration channel initialization.
""",
    )

    replace_exact(
        main_rs,
        """        call::init(app_state.client.clone(), app_state.user_store.clone(), cx);
        notifications::init(app_state.client.clone(), app_state.user_store.clone(), cx);
        collab_ui::init(&app_state, cx);
""",
        """        // Eqavo disables upstream call, notification, and collaboration UI initialization.
""",
    )

    replace_exact(
        zed_rs,
        """        let channels_panel =
            collab_ui::collab_panel::CollabPanel::load(workspace_handle.clone(), cx.clone());
        let notification_panel = collab_ui::notification_panel::NotificationPanel::load(
            workspace_handle.clone(),
            cx.clone(),
        );
""",
        """        // Eqavo disables collaboration and notification panel loading.
""",
    )

    replace_exact(
        zed_rs,
        """            add_panel_when_ready(channels_panel, workspace_handle.clone(), cx.clone()),
            add_panel_when_ready(notification_panel, workspace_handle.clone(), cx.clone()),
""",
        """            // Eqavo disables collaboration and notification panels.
""",
    )

    print("Applied Eqavo service stripping profile.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
