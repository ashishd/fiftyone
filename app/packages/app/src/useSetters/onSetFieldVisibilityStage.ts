import {
  setFieldVisibilityStage,
  type setFieldVisibilityStageMutation,
  subscribeBefore,
} from "@fiftyone/relay";
import { type State, stateSubscription } from "@fiftyone/state";
import { DefaultValue } from "recoil";
import { commitMutation } from "relay-runtime";
import { pendingEntry } from "../Renderer";
import { resolveURL } from "../utils";
import type { RegisteredSetter } from "./registerSetter";

const onSetFieldVisibilityStage: RegisteredSetter =
  ({ environment, router, sessionRef }) =>
  ({ get, set }, input?: DefaultValue | State.FieldVisibilityStage) => {
    set(pendingEntry, true);
    const newValue = input instanceof DefaultValue ? undefined : input;
    const stage = newValue
      ? {
          _cls: newValue.cls || "fiftyone.core.stages.ExcludeFields",
          kwargs: {
            field_names: newValue.kwargs?.field_names || [],
            _allow_missing: true,
          },
        }
      : undefined;

    const unsubscribe = subscribeBefore(() => {
      sessionRef.current.fieldVisibilityStage = newValue;
      unsubscribe();
    });

    // reload page query with new extended view
    router.history.replace(
      resolveURL({
        currentPathname: router.history.location.pathname,
        currentSearch: router.history.location.search,
      }),
      {
        ...router.get().state,
        fieldVisibility: stage,
      }
    );

    // send event as side effect
    commitMutation<setFieldVisibilityStageMutation>(environment, {
      mutation: setFieldVisibilityStage,
      variables: {
        stage,
        subscription: get(stateSubscription),
      },
    });
  };

export default onSetFieldVisibilityStage;
