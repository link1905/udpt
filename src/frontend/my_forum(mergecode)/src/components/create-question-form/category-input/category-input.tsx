import { Select, SelectProps } from "@mantine/core";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import { requestCreateCategory } from "../../../services/forum/create-category.ts";
import {
  getAllCategoriesQueryKey,
  requestGetAllCategories,
} from "../../../services/forum/get-all-tags.ts";
import { Item } from "../tags-input";

export interface TagsInputProps
  extends Partial<Omit<SelectProps, "value" | "onChange">> {
  value: number;
  onChange: (value: number) => void;
}

export function CategoryInput({ value, onChange, ...props }: TagsInputProps) {
  const queryClient = useQueryClient();
  const { mutate } = useMutation(requestCreateCategory, {
    onSuccess(tagModel) {
      onChange(tagModel.pk);
      return queryClient.invalidateQueries(getAllCategoriesQueryKey);
    },
  });
  const { data } = useQuery(getAllCategoriesQueryKey, requestGetAllCategories, {
    select: (data) =>
      data.results.map((data) => ({
        label: data.fields.name,
        value: String(data.pk),
      })),
  });
  return (
    <Select
      {...props}
      value={String(value)}
      onChange={(value) => onChange(Number(value))}
      creatable
      getCreateLabel={(query) => `+ Create category ${query}`}
      onCreate={(query) => {
        mutate({
          name: query,
        });
        return null;
      }}
      data={data || []}
      limit={20}
      itemComponent={Item}
      searchable
      placeholder="Category"
    />
  );
}
