import { forumServiceClient, CategoryFields } from "./forum.client.ts";
import { Model } from "../client.ts";

export const requestGetCategory = (id: string | number) =>
  forumServiceClient
    .get<Model<CategoryFields>>(
      `/models/thread-categories/records/${id}/`,
    )
    .then((res) => res.data);

export const getCategoryQueryKey = (id: string | number) =>
  ["thread-category", String(id)] as const;
