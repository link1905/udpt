import {Badge, Text} from "@mantine/core";
import { useQuery } from "@tanstack/react-query";
import {
  getCategoryQueryKey,
  requestGetCategory,
} from "../../services/forum/get-category.ts";

export function ThreadCategory({ id }: { id: string | number }) {
  const { data } = useQuery(getCategoryQueryKey(id), () =>
    requestGetCategory(id),
  );
  return <Badge color="red" radius="lg" variant="filled" className="ml-[-5px] p-[13px]">{data?.fields?.name}</Badge>;
}
