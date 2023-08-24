import { useQuery } from "@tanstack/react-query";
import {
  getAllThreadsQueryKey,
  requestGetAllThreads,
} from "../../services/forum/get-all-threads.ts";
import {
  ActionIcon,
  Avatar,
  Box,
  Divider,
  Group,
  Paper,
  Stack,
  Text,
} from "@mantine/core";
import { IconThumbDown, IconThumbUp } from "@tabler/icons-react";
import demoAvatarImage from "../../assets/avata.jpeg";
import { ThreadComments } from "../thread-comments";
import { ThreadVotes } from "../thread-votes/thread-votes.tsx";
import { UserAvatar } from "../user-avatar/user-avatar.tsx";

export function ThreadAnswers({ id }: { id: string }) {
  const { data } = useQuery(getAllThreadsQueryKey(id), () =>
    requestGetAllThreads(id)
  );
  return (
    <Stack>
      {data &&
        data.results.map((threadModel) => (
          <Paper key={threadModel.pk} withBorder p="xl" mb="xl">
            <Group align="start">
              <Box>
                <ThreadVotes id={threadModel.pk} />
              </Box>
              <Box sx={{ flex: 1 }}>
                <Stack align="start">
                  <Text>Answer at {threadModel?.fields?.created}</Text>
                  {threadModel?.fields?.creator_id && (
                    <UserAvatar id={threadModel?.fields?.creator_id} />
                  )}
                  <Box>
                  
                    {threadModel?.fields?.approved ? (
                      <div
                        dangerouslySetInnerHTML={{
                          __html: threadModel.fields.content,
                        }}
                      />
                    ) : (
                      <div
                        className="opacity-50" // Thêm lớp để hiển thị mờ
                        dangerouslySetInnerHTML={{
                          __html: threadModel.fields.content,
                        }}
                      />
                    )}
                  </Box>
                  {/* Hiển thị trạng thái */}
                  {threadModel?.fields?.approved ? (
                    <Text className="text-[14px] font-bold" color="green">
                      Đã duyệt
                    </Text>
                  ) : (
                    <Text className="text-[14px] font-bold" color="red">
                      Đợi duyệt
                    </Text>
                  )}
                </Stack>
                <Divider my="md" />
                <ThreadComments id={threadModel.pk} />
              </Box>
            </Group>
          </Paper>
        ))}
    </Stack>
  );
}
