import { Box, Stack, Text } from "@mantine/core";
import { useQuery } from "@tanstack/react-query";
import {
  getAllThreadsQueryKey,
  requestGetAllThreads,
} from "../../services/forum/get-all-threads.ts";
import { AnswerForm } from "../answer-form";
import { UserAvatar } from "../user-avatar/user-avatar.tsx";

export function ThreadComments({ id }: { id: string | number }) {
  const { data } = useQuery(getAllThreadsQueryKey(id), () =>
    requestGetAllThreads(id),
  );
  return (
    <Stack>
      {data &&
        data.results.map((threadModel) => (
          <Stack key={threadModel.pk}>
            <UserAvatar id={threadModel?.fields?.creator_id} />
            <Text>Commented at {threadModel?.fields?.created}</Text>
            <Box>
              {threadModel?.fields?.content && (
                <div
                  dangerouslySetInnerHTML={{
                    __html: threadModel.fields.content,
                  }}
                />
              )}
            </Box>
          </Stack>
        ))}
      <AnswerForm id={id} title="Comment" />
    </Stack>
  );
}
