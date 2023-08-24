import { TagFields, tagServiceClient } from "./tag.client.ts";
import { Model } from "../client.ts";

export const requestCreateTag = (data: Pick<TagFields, "name">) =>
  tagServiceClient
    .post<Model<TagFields>>("/models/tags/records/", data)
    .then((res) => res.data);
