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
    if new in content:
        return
    if old not in content:
        raise RuntimeError(f"Expected snippet not found in {path}")
    path.write_text(content.replace(old, new, 1))


def replace_between(path: Path, start_marker: str, end_marker: str, replacement: str) -> None:
    content = path.read_text()
    if replacement in content:
        return
    start = content.find(start_marker)
    if start == -1:
        raise RuntimeError(f"Start marker not found in {path}: {start_marker}")
    end = content.find(end_marker, start)
    if end == -1:
        raise RuntimeError(f"End marker not found in {path}: {end_marker}")
    path.write_text(content[:start] + replacement + content[end:])


def main() -> int:
    paths = load_paths(ROOT)
    main_rs = paths.source_dir / "crates" / "zed" / "src" / "main.rs"
    zed_rs = paths.source_dir / "crates" / "zed" / "src" / "zed.rs"
    title_bar_rs = paths.source_dir / "crates" / "title_bar" / "src" / "title_bar.rs"

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
        main_rs,
        """        telemetry.flush_events().detach();
""",
        """        // Eqavo disables upstream telemetry flushing.
""",
    )

    replace_exact(
        main_rs,
        """        cx.spawn({
            let client = app_state.client.clone();
            async move |cx| authenticate(client, cx).await
        })
        .detach_and_log_err(cx);
""",
        """        // Eqavo disables automatic upstream account sign-in on startup.
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

    replace_exact(
        title_bar_rs,
        """                .when(
                    user.is_none() && TitleBarSettings::get_global(cx).show_sign_in,
                    |this| this.child(self.render_sign_in_button(cx)),
                )
""",
        "",
    )

    replace_between(
        title_bar_rs,
        "    pub fn render_sign_in_button(&mut self, _: &mut Context<Self>) -> Button {\n",
        "    pub fn render_user_menu_button(&mut self, cx: &mut Context<Self>) -> impl Element {\n",
        """    pub fn render_sign_in_button(&mut self, _: &mut Context<Self>) -> Button {
        Button::new("sign_in_disabled", "已禁用")
            .label_size(LabelSize::Small)
            .disabled(true)
    }

""",
    )

    replace_between(
        title_bar_rs,
        "    pub fn render_user_menu_button(&mut self, cx: &mut Context<Self>) -> impl Element {\n",
        "            .anchor(Corner::TopRight)\n",
        """    pub fn render_user_menu_button(&mut self, cx: &mut Context<Self>) -> impl Element {
        let trigger =
            ButtonLike::new("user-menu").child(Icon::new(IconName::ChevronDown).size(IconSize::Small));

        PopoverMenu::new("user-menu")
            .trigger(trigger)
            .menu(move |window, cx| {
                ContextMenu::build(window, cx, |menu, _, _cx| {
                    menu
                        .action("设置", zed_actions::OpenSettings.boxed_clone())
                        .action("Keymap", Box::new(zed_actions::OpenKeymap))
                        .action(
                            "Themes…",
                            zed_actions::theme_selector::Toggle::default().boxed_clone(),
                        )
                        .action(
                            "Icon Themes…",
                            zed_actions::icon_theme_selector::Toggle::default().boxed_clone(),
                        )
                        .action(
                            "扩展",
                            zed_actions::Extensions::default().boxed_clone(),
                        )
                })
                .into()
            })
""",
    )

    print("Applied Eqavo service stripping profile.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
