import { Model } from "../client.ts";
import { CategoryFields, forumServiceClient } from "./forum.client.ts";

export const requestCreateCategory = (data: Pick<CategoryFields, "name">) =>
  forumServiceClient
    .post<Model<CategoryFields>>("/models/thread-categories/records/", data)
    .then((res) => res.data);
