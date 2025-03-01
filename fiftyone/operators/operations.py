"""
FiftyOne operator execution.

| Copyright 2017-2024, Voxel51, Inc.
| `voxel51.com <https://voxel51.com/>`_
|
"""

import json

from bson import json_util


class Operations(object):
    """Interface to trigger builtin operations on an execution context.

    Args:
        ctx: an :class:`fiftyone.operators.executor.ExecutionContext`
    """

    def __init__(self, ctx):
        self._ctx = ctx

    ###########################################################################
    # Builtin Python operators
    ###########################################################################

    def clone_selected_samples(self):
        """Clone the selected samples in the App."""
        return self._ctx.trigger("clone_selected_samples")

    def clone_sample_field(self, field_name, new_field_name):
        """Clone a sample field to a new field name.

        Args:
            field_name: the name of the field to clone
            new_field_name: the name for the new field
        """
        return self._ctx.trigger(
            "clone_sample_field",
            params={
                "field_name": field_name,
                "new_field_name": new_field_name,
            },
        )

    def rename_sample_field(self, field_name, new_field_name):
        """Rename a sample field to a new field name.

        Args:
            field_name: the name of the field to rename
            new_field_name: the new name for the field
        """
        return self._ctx.trigger(
            "rename_sample_field",
            params={
                "field_name": field_name,
                "new_field_name": new_field_name,
            },
        )

    def clear_sample_field(self, field_name):
        """Clear the contents of a sample field.

        Args:
            field_name: the name of the field to clear
        """
        return self._ctx.trigger(
            "clear_sample_field",
            params={"field_name": field_name},
        )

    def delete_selected_samples(self):
        """Delete the selected samples in the App."""
        return self._ctx.trigger("delete_selected_samples")

    def delete_selected_labels(self):
        """Delete the selected labels in the App."""
        return self._ctx.trigger("delete_selected_labels")

    def delete_sample_field(self, field_name):
        """Delete a sample field.

        Args:
            field_name: the name of the field to delete
        """
        return self._ctx.trigger(
            "delete_sample_field",
            params={"field_name": field_name},
        )

    def print_stdout(self, message):
        """Print a message to the standard output.

        Args:
            message: the message to print
        """
        return self._ctx.trigger("print_stdout", params={"msg": message})

    def list_files(self, path=None, list_filesystems=False):
        """List files in a directory or list filesystems.

        Args:
            path (None): the path to list files from, or None to list
                filesystems
            list_filesystems (False): whether to list filesystems instead of
                files
        """
        return self._ctx.trigger(
            "list_files",
            params={"path": path, "list_filesystems": list_filesystems},
        )

    ###########################################################################
    # Builtin JS operators
    ###########################################################################

    def reload_samples(self):
        """Reload the sample grid in the App."""
        return self._ctx.trigger("reload_samples")

    def reload_dataset(self):
        """Reload the dataset in the App."""
        return self._ctx.trigger("reload_dataset")

    def clear_selected_samples(self):
        """Clear selected samples in the App."""
        return self._ctx.trigger("clear_selected_samples")

    def copy_view_as_json(self):
        """Copy the current view in the App as JSON."""
        return self._ctx.trigger("copy_view_as_json")

    def view_from_json(self):
        """Set the view in the App from JSON present in clipboard."""
        return self._ctx.trigger("view_from_clipboard")

    def _create_panel_params(self, panel_id, state=None, data=None):
        params = {"panel_id": panel_id}
        if panel_id is None:
            params["panel_id"] = self._ctx.params.get("panel_id", None)
        if state is not None:
            params["state"] = state
        if data is not None:
            params["data"] = data
        return params

    def clear_panel_state(self, panel_id=None):
        """Clear the state of the specified panel in the App.

        Args:
            panel_id (None): the optional ID of the panel to clear.
                If not provided, the ctx.current_panel.id will be used.
        """
        return self._ctx.trigger(
            "clear_panel_state", params=self._create_panel_params(panel_id)
        )

    def clear_panel_data(self, panel_id=None):
        """Clear the data of the specified panel in the App.

        Args:
            panel_id (None): the optional ID of the panel to clear.
                If not provided, the ctx.current_panel.id will be used.
        """
        return self._ctx.trigger(
            "clear_panel_data", params=self._create_panel_params(panel_id)
        )

    def set_panel_state(self, state, panel_id=None):
        """Set the entire state of the specified panel in the App.

        Args:
            panel_id (None): the optional ID of the panel to clear.
                If not provided, the ctx.current_panel.id will be used.
            state (dict): the state to set
        """
        return self._ctx.trigger(
            "set_panel_state",
            params=self._create_panel_params(panel_id, state=state),
        )

    def set_panel_data(self, data, panel_id=None):
        """Set the entire data of the specified panel in the App.

        Args:
            panel_id (None): the optional ID of the panel to clear.
                If not provided, the ctx.current_panel.id will be used.
            data (dict): the data to set
        """
        return self._ctx.trigger(
            "set_panel_data",
            params=self._create_panel_params(panel_id, data=data),
        )

    def patch_panel_state(self, state, panel_id=None):
        """Patch the state of the specified panel in the App.

        Args:
            panel_id (None): the optional ID of the panel to clear.
                If not provided, the ctx.current_panel.id will be used.
        """
        return self._ctx.trigger(
            "patch_panel_state",
            params=self._create_panel_params(panel_id, state=state),
        )

    def patch_panel_data(self, data, panel_id=None):
        """Patch the state of the specified panel in the App.

        Args:
            panel_id (None): the optional ID of the panel to clear.
                If not provided, the ctx.current_panel.id will be used.
        """
        return self._ctx.trigger(
            "patch_panel_data",
            params=self._create_panel_params(panel_id, data=data),
        )

    def reduce_panel_state(self, reducer, panel_id=None):
        """Reduce the state of the specified panel in the App.

        Args:
            panel_id (None): the optional ID of the panel to clear.
                If not provided, the ctx.current_panel.id will be used.
        """
        return self._ctx.trigger(
            "reduce_panel_state",
            params={
                **self._create_panel_params(panel_id),
                "reducer": reducer,
            },
        )

    def show_panel_output(self, output, panel_id=None):
        """Show output in the specified panel in the App.

        Args:
            output: the output to show
            panel_id (None): the optional ID of the panel to clear.
                If not provided, the ctx.current_panel.id will be used.
        """
        params = self._create_panel_params(panel_id)
        return self._ctx.trigger(
            "show_panel_output",
            params={
                **params,
                "output": output.to_json(),
            },
        )

    def open_panel(
        self,
        name,
        is_active=True,
        layout=None,
        force=False,
        force_duplicate=False,
    ):
        """Open a panel with the given name and layout options in the App.

        Args:
            name: the name of the panel to open
            is_active (True): whether to activate the panel immediately
            layout (None): the layout orientation
                ``("horizontal", "vertical")``, if applicable
            force (False): whether to force open the panel. Skips the check to see if a panel with
                the same name exists or not. Note: this also skips allowDuplicates check
            force_duplicate (False): whether to force open the panel even if it is already open.
                Only applicable if force is ``True``
        """
        params = {
            "name": name,
            "isActive": is_active,
            "force": force,
            "forceDuplicate": force_duplicate,
        }
        if layout is not None:
            params["layout"] = layout

        return self._ctx.trigger("open_panel", params=params)

    def register_panel(
        self,
        name,
        label,
        icon=None,
        dark_icon=None,
        light_icon=None,
        on_load=None,
        on_unload=None,
        on_change=None,
        on_change_ctx=None,
        on_change_view=None,
        on_change_dataset=None,
        on_change_current_sample=None,
        on_change_selected=None,
        on_change_selected_labels=None,
        on_change_extended_selection=None,
        allow_duplicates=False,
    ):
        """Register a panel with the given name and lifecycle callbacks.

        Args:
            name: the name of the panel to register
            icon (None): the icon to display in the panel tab
            dark_icon (None): the icon to display in the panel tab in dark mode of app
            light_icon (None): the icon to display in the panel tab in light mode of app
            on_load (None): an operator to invoke when the panel is loaded
            on_unload (None): an operator to invoke when the panel is unloaded
            on_change (None): an operator to invoke when the panel state changes
            allow_duplicates (False): whether to allow multiple instances of the panel
        """
        params = {
            "panel_name": name,
            "panel_label": label,
            "icon": icon,
            "dark_icon": dark_icon,
            "light_icon": light_icon,
            "on_load": on_load,
            "on_unload": on_unload,
            "on_change": on_change,
            "allow_duplicates": allow_duplicates,
            "on_change_ctx": on_change_ctx,
            "on_change_view": on_change_view,
            "on_change_dataset": on_change_dataset,
            "on_change_current_sample": on_change_current_sample,
            "on_change_selected": on_change_selected,
            "on_change_selected_labels": on_change_selected_labels,
            "on_change_extended_selection": on_change_extended_selection,
        }
        return self._ctx.trigger("register_panel", params=params)

    def open_all_panels(self):
        """Open all available panels in the App."""
        return self._ctx.trigger("open_all_panel")

    def close_panel(self, name=None, id=None):
        """Close the panel with the given name in the App.

        Args:
            name: the name of the panel to close
            id: the id of the panel to close
        """
        return self._ctx.trigger(
            "close_panel", params={"name": name, "id": id}
        )

    def close_all_panels(self):
        """Close all open panels in the App."""
        return self._ctx.trigger("close_all_panel")

    def split_panel(self, name, layout):
        """Split the panel with the given layout in the App.

        Args:
            name: the name of the panel to split
            layout: the layout orientation ``("horizontal", "vertical")``
        """
        return self._ctx.trigger(
            "split_panel", params={"name": name, "layout": layout}
        )

    def open_dataset(self, dataset_name):
        """Open the specified dataset in the App.

        Args:
            dataset_name: the name of the dataset to open
        """
        return self._ctx.trigger(
            "open_dataset", params={"dataset": dataset_name}
        )

    def clear_view(self):
        """Clear the view bar in the App."""
        return self._ctx.trigger("clear_view")

    def clear_sidebar_filters(self):
        """Clear all filters in the App's sidebar."""
        return self._ctx.trigger("clear_sidebar_filters")

    def clear_all_stages(self):
        """Clear all selections, filters, and view stages from the App."""
        return self._ctx.trigger("clear_all_stages")

    def refresh_colors(self):
        """Refresh the colors used in the App's UI."""
        return self._ctx.trigger("refresh_colors")

    def show_selected_samples(self):
        """Show the samples that are currently selected in the App."""
        return self._ctx.trigger("show_selected_samples")

    def convert_extended_selection_to_selected_samples(self):
        """Convert the extended selection to selected samples in the App."""
        return self._ctx.trigger(
            "convert_extended_selection_to_selected_samples"
        )

    def set_selected_samples(self, samples):
        """Select the specified samples in the App.

        Args:
            samples: a list of sample IDs to select
        """
        return self._ctx.trigger(
            "set_selected_samples", params={"samples": samples}
        )

    def set_view(self, view=None, name=None):
        """Set the current view in the App.

        Args:
            view (None): a :class:`fiftyone.core.view.DatasetView` to load
            name (None): the name of a saved view to load
        """
        params = {}
        if view is not None:
            params["view"] = _serialize_view(view)

        if name is not None:
            params["name"] = name

        return self._ctx.trigger("set_view", params=params)

    def show_samples(self, samples, use_extended_selection=False):
        """Show specific samples, optionally using extended selection in the
        App.

        Args:
            samples: a list of sample IDs to show
            use_extended_selection (False): whether to use the extended
                selection feature
        """
        params = {
            "samples": samples,
            "use_extended_selection": use_extended_selection,
        }
        return self._ctx.trigger("show_samples", params=params)

    def console_log(self, message):
        """Log a message to the console.

        Args:
            message: the message to log
        """
        return self._ctx.trigger("console_log", params={"message": message})

    def show_output(self, outputs, results):
        """Show output in the App's UI.

        Args:
            outputs: outputs to show
            results: results to display
        """
        return self._ctx.trigger(
            "show_output", params={"outputs": outputs, "results": results}
        )

    def set_progress(self, label=None, progress=None, variant=None):
        """Set the progress indicator in the App's UI.

        Args:
            label (None): a label for the progress indicator
            progress (None): a progress value to set
            variant (None): the type of indicator ``("linear", "circular")``
        """
        params = {}
        if label is not None:
            params["label"] = label
        if progress is not None:
            params["progress"] = progress
        if variant is not None:
            params["variant"] = variant

        return self._ctx.trigger("set_progress", params=params)

    def test_operator(self, operator, raw_params):
        """Test the operator with given parameters.

        Args:
            operator: the operator to test
            raw_params: raw parameters for the operator
        """
        return self._ctx.trigger(
            "test_operator",
            params={"operator": operator, "raw_params": raw_params},
        )

    def set_selected_labels(self, labels):
        """Set the selected labels in the App.

        Args:
            labels: the labels to select
        """
        return self._ctx.trigger(
            "set_selected_labels", params={"labels": labels}
        )

    def clear_selected_labels(self):
        """Clear the selected labels in the App."""
        return self._ctx.trigger("clear_selected_labels")

    def notify(self, message, variant="info"):
        """Show a notification in the App.

        Variants are "info", "success", "warning", and "error".

        Args:
            message: the message to show
            variant ("info"): the type of notification
        """
        return self._ctx.trigger(
            "notify", params={"message": message, "variant": variant}
        )

    def set_extended_selection(
        self, selection=None, scope=None, clear=False, reset=False
    ):
        """Set the extended selection in the App.

        Args:
            selection: the selection to set
            scope: the scope of the selection
            clear: whether to clear the selection
            reset: whether to reset the selection
        """
        return self._ctx.trigger(
            "set_extended_selection",
            params={
                "selection": selection,
                "scope": scope,
                "clear": clear,
                "reset": reset,
            },
        )

    def set_spaces(self, spaces=None, name=None):
        """Set space in the App by name or :class:`fiftyone.core.odm.workspace.Space`.

        Args:
            spaces: the spaces (:class:`fiftyone.core.odm.workspace.Space`) to load
            name: the name of the workspace to load
        """
        params = {}
        if spaces is not None:
            params["spaces"] = spaces.to_dict()
        elif name is not None:
            params["spaces"] = self._ctx.dataset.load_workspace(name).to_dict()

        return self._ctx.trigger("set_spaces", params=params)

    def set_active_fields(self, fields=[]):
        """Set the active fields in the App.

        Args:
            fields: the fields to set such as "ground_truth", "metadata.width", etc.
        """
        return self._ctx.trigger(
            "set_active_fields", params={"fields": fields}
        )

    def track_event(self, event, properties=None):
        """Track an event in the App.

        Args:
            event: the event to track
            properties (None): the properties to track
        """
        return self._ctx.trigger(
            "track_event", params={"event": event, "properties": properties}
        )

    def set_panel_title(self, id=None, title=None):
        """Set the title of the specified panel in the App.

        Args:
            id: the ID of the panel to set the title
            title: the title to set
        """
        return self._ctx.trigger(
            "set_panel_title", params={"id": id, "title": title}
        )


def _serialize_view(view):
    return json.loads(json_util.dumps(view._serialize()))
