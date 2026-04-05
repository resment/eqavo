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
    if new and new in content:
        return
    if not new and old not in content:
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
    language_models_rs = paths.source_dir / "crates" / "language_models" / "src" / "language_models.rs"
    agent_panel_onboarding_rs = (
        paths.source_dir / "crates" / "ai_onboarding" / "src" / "agent_panel_onboarding_content.rs"
    )
    edit_prediction_onboarding_rs = (
        paths.source_dir / "crates" / "ai_onboarding" / "src" / "edit_prediction_onboarding_content.rs"
    )
    agent_panel_rs = paths.source_dir / "crates" / "agent_ui" / "src" / "agent_panel.rs"
    thread_view_rs = (
        paths.source_dir / "crates" / "agent_ui" / "src" / "conversation_view" / "thread_view.rs"
    )
    text_thread_editor_rs = (
        paths.source_dir / "crates" / "agent_ui" / "src" / "text_thread_editor.rs"
    )
    edit_prediction_button_rs = (
        paths.source_dir / "crates" / "edit_prediction_ui" / "src" / "edit_prediction_button.rs"
    )
    edit_prediction_registry_rs = (
        paths.source_dir / "crates" / "zed" / "src" / "zed" / "edit_prediction_registry.rs"
    )

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

    replace_exact(
        language_models_rs,
        "use crate::provider::cloud::CloudLanguageModelProvider;\n",
        "",
    )

    replace_exact(
        language_models_rs,
        """    registry.register_provider(
        Arc::new(CloudLanguageModelProvider::new(
            user_store,
            client.clone(),
            cx,
        )),
        cx,
    );
""",
        """    let _ = user_store;
""",
    )

    replace_exact(
        agent_panel_onboarding_rs,
        """impl Render for AgentPanelOnboarding {
    fn render(&mut self, _window: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        let enrolled_in_trial = self
            .user_store
            .read(cx)
            .plan()
            .is_some_and(|plan| plan == Plan::ZedProTrial);
        let is_pro_user = self
            .user_store
            .read(cx)
            .plan()
            .is_some_and(|plan| plan == Plan::ZedPro);

        AgentPanelOnboardingCard::new()
            .child(
                ZedAiOnboarding::new(
                    self.client.clone(),
                    &self.user_store,
                    self.continue_with_zed_ai.clone(),
                    cx,
                )
                .with_dismiss({
                    let callback = self.continue_with_zed_ai.clone();
                    move |window, cx| callback(window, cx)
                }),
            )
            .map(|this| {
                if enrolled_in_trial || is_pro_user || self.has_configured_providers {
                    this
                } else {
                    this.child(ApiKeysWithoutProviders::new())
                }
            })
    }
}
""",
        """impl Render for AgentPanelOnboarding {
    fn render(&mut self, _window: &mut Window, _cx: &mut Context<Self>) -> impl IntoElement {
        AgentPanelOnboardingCard::new().child(ApiKeysWithoutProviders::new())
    }
}
""",
    )

    replace_exact(
        edit_prediction_onboarding_rs,
        """use client::{Client, UserStore};
use cloud_api_types::Plan;
use gpui::{Entity, IntoElement, ParentElement};
use ui::prelude::*;

use crate::ZedAiOnboarding;
""",
        """use client::{Client, UserStore};
use cloud_api_types::Plan;
use gpui::{Entity, IntoElement, ParentElement};
use ui::prelude::*;
""",
    )

    replace_exact(
        edit_prediction_onboarding_rs,
        """impl Render for EditPredictionOnboarding {
    fn render(&mut self, _window: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        let is_free_plan = self
            .user_store
            .read(cx)
            .plan()
            .is_some_and(|plan| plan == Plan::ZedFree);

        let github_copilot = v_flex()
            .gap_1()
            .child(Label::new(if self.copilot_is_configured {
                "Alternatively, you can continue to use GitHub Copilot as that's already set up."
            } else {
                "Alternatively, you can use GitHub Copilot as your edit prediction provider."
            }))
            .child(
                Button::new(
                    "configure-copilot",
                    if self.copilot_is_configured {
                        "Use Copilot"
                    } else {
                        "Configure Copilot"
                    },
                )
                .full_width()
                .style(ButtonStyle::Outlined)
                .on_click({
                    let callback = self.continue_with_copilot.clone();
                    move |_, window, cx| callback(window, cx)
                }),
            );

        v_flex()
            .gap_2()
            .child(ZedAiOnboarding::new(
                self.client.clone(),
                &self.user_store,
                self.continue_with_zed_ai.clone(),
                cx,
            ))
            .when(is_free_plan, |this| {
                this.child(ui::Divider::horizontal()).child(github_copilot)
            })
    }
}
""",
        """impl Render for EditPredictionOnboarding {
    fn render(&mut self, _window: &mut Window, cx: &mut Context<Self>) -> impl IntoElement {
        let is_free_plan = self
            .user_store
            .read(cx)
            .plan()
            .is_some_and(|plan| plan == Plan::ZedFree);

        let github_copilot = v_flex()
            .gap_1()
            .child(Label::new(if self.copilot_is_configured {
                "Alternatively, you can continue to use GitHub Copilot as that's already set up."
            } else {
                "Alternatively, you can use GitHub Copilot as your edit prediction provider."
            }))
            .child(
                Button::new(
                    "configure-copilot",
                    if self.copilot_is_configured {
                        "Use Copilot"
                    } else {
                        "Configure Copilot"
                    },
                )
                .full_width()
                .style(ButtonStyle::Outlined)
                .on_click({
                    let callback = self.continue_with_copilot.clone();
                    move |_, window, cx| callback(window, cx)
                }),
            );

        v_flex()
            .gap_2()
            .child(
                Label::new(
                    "Eqavo does not include Zed AI. Configure your own edit prediction provider instead.",
                )
                .color(Color::Muted),
            )
            .when(is_free_plan, |this| this.child(ui::Divider::horizontal()).child(github_copilot))
    }
}
""",
    )

    replace_between(
        agent_panel_rs,
        "        let zed_provider_configured = AgentSettings::get_global(cx)\n",
        "        match configuration_error {\n",
        """        let zed_provider_configured = AgentSettings::get_global(cx)
            .default_model
            .as_ref()
            .is_some_and(|selection| selection.provider.0.as_str() == "zed.dev");

        let callout = if zed_provider_configured {
            Callout::new()
                .icon(IconName::Warning)
                .severity(Severity::Warning)
                .when(border_bottom, |this| {
                    this.border_position(ui::BorderPosition::Bottom)
                })
                .title("Eqavo does not include Zed AI.")
                .description("Select another model provider in the configuration panel.")
                .actions_slot(
                    Button::new("settings", "Configure")
                        .style(ButtonStyle::Tinted(ui::TintColor::Warning))
                        .label_size(LabelSize::Small)
                        .key_binding(
                            KeyBinding::for_action_in(&OpenSettings, focus_handle, cx)
                                .map(|kb| kb.size(rems_from_px(12.))),
                        )
                        .on_click(|_event, window, cx| {
                            window.dispatch_action(OpenSettings.boxed_clone(), cx)
                        }),
                )
        } else {
            Callout::new()
                .icon(IconName::Warning)
                .severity(Severity::Warning)
                .when(border_bottom, |this| {
                    this.border_position(ui::BorderPosition::Bottom)
                })
                .title(configuration_error.to_string())
                .actions_slot(
                    Button::new("settings", "Configure")
                        .style(ButtonStyle::Tinted(ui::TintColor::Warning))
                        .label_size(LabelSize::Small)
                        .key_binding(
                            KeyBinding::for_action_in(&OpenSettings, focus_handle, cx)
                                .map(|kb| kb.size(rems_from_px(12.))),
                        )
                        .on_click(|_event, window, cx| {
                            window.dispatch_action(OpenSettings.boxed_clone(), cx)
                        }),
                )
        };
""",
    )

    replace_between(
        thread_view_rs,
        "    fn render_payment_required_error(&self, cx: &mut Context<Self>) -> Callout {\n",
        "    fn authenticate_button(&self, cx: &mut Context<Self>) -> impl IntoElement {\n",
        """    fn render_payment_required_error(&self, cx: &mut Context<Self>) -> Callout {
        const ERROR_MESSAGE: &str =
            "Eqavo does not include Zed AI billing. Choose another provider to continue.";

        Callout::new()
            .severity(Severity::Error)
            .icon(IconName::XCircle)
            .title("Provider Unavailable")
            .description(ERROR_MESSAGE)
            .actions_slot(h_flex().gap_0p5().child(self.create_copy_button(ERROR_MESSAGE)))
            .dismiss_action(self.dismiss_error_button(cx))
    }

    fn upgrade_button(&self, _cx: &mut Context<Self>) -> impl IntoElement {
        Button::new("upgrade_disabled", "Unavailable")
            .label_size(LabelSize::Small)
            .disabled(true)
    }

""",
    )

    replace_between(
        text_thread_editor_rs,
        '    fn render_payment_required_error(&self, cx: &mut Context<Self>) -> AnyElement {\n',
        "    fn render_assist_error(\n",
        """    fn render_payment_required_error(&self, cx: &mut Context<Self>) -> AnyElement {
        const ERROR_MESSAGE: &str =
            "Eqavo does not include Zed AI billing. Choose another provider to continue.";

        v_flex()
            .gap_0p5()
            .child(
                h_flex()
                    .gap_1p5()
                    .items_center()
                    .child(Icon::new(IconName::XCircle).color(Color::Error))
                    .child(Label::new("Provider Unavailable").weight(FontWeight::MEDIUM)),
            )
            .child(
                div()
                    .id("error-message")
                    .max_h_24()
                    .overflow_y_scroll()
                    .child(Label::new(ERROR_MESSAGE)),
            )
            .child(
                h_flex()
                    .justify_end()
                    .mt_1()
                    .child(Button::new("dismiss", "Dismiss").on_click(cx.listener(
                        |this, _, _window, cx| {
                            this.last_error = None;
                            cx.notify();
                        },
                    ))),
            )
            .into_any()
    }
""",
    )

    replace_exact(
        edit_prediction_button_rs,
        "    providers.push(EditPredictionProvider::Zed);\n",
        "    // Eqavo does not expose the upstream Zed AI edit prediction provider.\n",
    )

    replace_exact(
        edit_prediction_button_rs,
        """            .separator()
            .entry("Use Zed AI", None, {
                let fs = fs.clone();
                move |_window, cx| {
                    set_completion_provider(fs.clone(), cx, EditPredictionProvider::Zed)
                }
            })
""",
        """            .separator()
""",
    )

    replace_exact(
        edit_prediction_registry_rs,
        """        EditPredictionProvider::Zed => {
            Some(EditPredictionProviderConfig::Zed(EditPredictionModel::Zeta))
        }
""",
        """        EditPredictionProvider::Zed => None,
""",
    )

    print("Applied Eqavo service stripping profile.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
