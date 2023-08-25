import { forumServiceClient, ThreadFields } from "./forum.client.ts";
import { ListResponse } from "../client.ts";
//export const requestGetAllThreads = (): Promise<ListResponse<ThreadFields>> =>
//forumServiceClient
//.get<ListResponse<ThreadFields>>(`/models/threads/records/`)
//.then((res) => res.data);

//requestGetAllThreads()
//.then((threadsResponse) => {
//const threads = threadsResponse.results;
//console.log(threads);
//})
//.catch((error) => {
//console.error("Error fetching threads:", error);
//});
//
export const requestGetAllThreads = (parent: string | number, order?: string) =>
  forumServiceClient
    .get<ListResponse<ThreadFields>>(
      `/models/threads/records/` + (parent ? `?parent=${parent}` : ""),
      {
        params: {
          include_approved_status: true,
          order: order || "",
        },
      }
    )
    .then((res) => res.data);

export const requestGetLatestThreads = (parent: string | number) =>
  forumServiceClient
    .get<ListResponse<ThreadFields>>(
      `/models/threads/records/` + (parent ? `?parent=${parent}` : ""),
      {
        params: {
          include_approved_status: true,
          ordering: "-fields.created",
        },
      }
    )
    .then((res) => res.data);

export const getAllThreadsQueryKey = (parent: string | number) =>
  parent ? ["thread", parent, "child"] : ["thread"];

export const requestGetListThreadsMostVotes = (
  parent: string | number,
  order?: string,
  limit?: number
) =>
  forumServiceClient
    .get<ListResponse<ThreadFields>>(
      `/models/threads/records/` + (parent ? `?parent=${parent}` : ""),
      {
        params: {
          include_approved_status: true,
          order: order || "",
          limit: limit || 0,
        },
      }
    )
    .then((res) => res.data);
