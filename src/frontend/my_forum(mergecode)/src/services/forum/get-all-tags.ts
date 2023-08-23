import { ListResponse } from "../client.ts";
import { CategoryFields, forumServiceClient } from "./forum.client.ts";

export const requestGetAllCategories = () =>
  forumServiceClient
    .get<ListResponse<CategoryFields>>("/models/thread-categories/records/")
    .then((res) => res.data);

export const getAllCategoriesQueryKey = ["thread-categories"] as const;
