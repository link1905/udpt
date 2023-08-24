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
  return <Badge>{data?.fields?.name}</Badge>;
}
