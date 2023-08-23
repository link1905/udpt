import { TagFields, tagServiceClient } from "./tag.client.ts";
import { ListResponse } from "../client.ts";

export const requestGetAllTags = () =>
  tagServiceClient
    .get<ListResponse<TagFields>>("/models/tags/records/")
    .then((res) => res.data);

export const getAllTagsQueryKey = ["tags"] as const;
