import { forumServiceClient } from "./forum.client";

export const requestDeleteTaggedThread = (pk: number) =>
  forumServiceClient
    .delete(`/models/tagged-threads/records/${pk}/`)
    .then((res) => res.data)
    .catch((error) => {
      throw new Error(`Error deleting tagged thread: ${error}`);
    });
