import { forwardRef } from "react";
import {
  MultiSelect,
  Box,
  CloseButton,
  SelectItemProps,
  MultiSelectValueProps,
  rem,
  Flex,
} from "@mantine/core";

const countriesData = [
  { label: "United States", value: "US" },
  { label: "Great Britain", value: "GB" },
  { label: "Finland", value: "FI" },
  { label: "France", value: "FR" },
  { label: "Russia", value: "RU" },
];

function Value({
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

const Item = forwardRef<HTMLDivElement, SelectItemProps>(
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

export function TagsInput() {
  return (
    <MultiSelect
      data={countriesData}
      limit={20}
      valueComponent={Value}
      itemComponent={Item}
      searchable
      placeholder="Tags"
    />
  );
}
