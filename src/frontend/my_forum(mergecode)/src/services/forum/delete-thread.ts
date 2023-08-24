import { forumServiceClient } from "./forum.client.ts";

export const requestDeleteThread = (id:number) =>
  forumServiceClient.delete(`/models/threads/records/${id}/`);