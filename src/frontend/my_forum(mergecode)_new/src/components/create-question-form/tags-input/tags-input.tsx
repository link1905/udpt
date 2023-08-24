import { forwardRef } from "react";
import {
  MultiSelect,
  Box,
  CloseButton,
  SelectItemProps,
  MultiSelectValueProps,
  rem,
  Flex,
  MultiSelectProps,
} from "@mantine/core";
import {
  getAllTagsQueryKey,
  requestGetAllTags,
} from "../../../services/tag/get-all-tags.ts";
import { requestCreateTag } from "../../../services/tag/create-tag.ts";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";

export function Value({
  // value,
  label,
  onRemove,
  // classNames,
  ...others
}: MultiSelectValueProps & { value: string }) {
  return (
    <div {...others}>
      <Box
        sx={(theme) => ({
          display: "flex",
          cursor: "default",
          alignItems: "center",
          backgroundColor:
            theme.colorScheme === "dark" ? theme.colors.dark[7] : theme.white,
          border: `${rem(1)} solid ${
            theme.colorScheme === "dark"
              ? theme.colors.dark[7]
              : theme.colors.gray[4]
          }`,
          paddingLeft: theme.spacing.xs,
          borderRadius: theme.radius.sm,
        })}
      >
        <Box sx={{ lineHeight: 1, fontSize: rem(12) }}>{label}</Box>
        <CloseButton
          onMouseDown={onRemove}
          variant="transparent"
          size={22}
          iconSize={14}
          tabIndex={-1}
        />
      </Box>
    </div>
  );
}

export const Item = forwardRef<HTMLDivElement, SelectItemProps>(
  (
    {
      label,
      // value,
      ...others
    },
    ref,
  ) => {
    return (
      <div ref={ref} {...others}>
        <Flex align="center">
          <div>{label}</div>
        </Flex>
      </div>
    );
  },
);

export interface TagsInputProps
  extends Partial<Omit<MultiSelectProps, "value" | "onChange">> {
  value: number[];
  onChange: (value: number[]) => void;
}

export function TagsInput({ onChange, value, ...props }: TagsInputProps) {
  const queryClient = useQueryClient();
  const { mutate } = useMutation(requestCreateTag, {
    onSuccess(tagModel) {
      onChange([...value, tagModel.pk]);
      return queryClient.invalidateQueries(getAllTagsQueryKey);
    },
  });
  const { data } = useQuery(getAllTagsQueryKey, requestGetAllTags, {
    select: (data) =>
      data.results.map((data) => ({
        label: data.fields.name,
        value: String(data.pk),
      })),
  });

  return (
    <MultiSelect
      {...props}
      value={value.map(String)}
      onChange={(value) => onChange(value.map(Number))}
      creatable
      getCreateLabel={(query) => `+ Create tag ${query}`}
      onCreate={(query) => {
        mutate({
          name: query,
        });
        return null;
      }}
      data={data || []}
      limit={20}
      valueComponent={Value}
      itemComponent={Item}
      searchable
      placeholder="Tags"
    />
  );
}
