import { tagServiceClient } from "./tag.client";

export const requestDeleteTag = (id: number) => {
  tagServiceClient.delete(`/models/tagged-threads/records/${id}`);
};
