import { NavLink, useParams } from "react-router-dom";
import {
  ActionIcon,
  Avatar,
  Badge,
  Box,
  Button,
  Group,
  LoadingOverlay,
  Paper,
  Stack,
  Text,
  Title,
} from "@mantine/core";
import { IconThumbUp, IconThumbDown } from "@tabler/icons-react";
import demoAvatarImage from "../../assets/avata.jpeg";
import { useQuery } from "@tanstack/react-query";
import {
  getThreadQueryKey,
  requestGetThread,
} from "../../services/forum/get-thread.ts";
import {
  requestGetThreadTags,
  threadTagsQueryKey,
} from "../../services/forum/get-thread-tags.ts";
import { AnswerForm } from "../../components/answer-form";
import { ThreadAnswers } from "../../components/thread-answers/thread-answers.tsx";
import { ThreadVotes } from "../../components/thread-votes/thread-votes.tsx";
import { UserAvatar } from "../../components/user-avatar/user-avatar.tsx";
import { ThreadCategory } from "../../components/thread-category/thread-category.tsx";
import { format } from "date-fns";
export function ViewQuestionPage() {
  

  const { id } = useParams<"id">();
  const { data, isLoading } = useQuery(
    getThreadQueryKey(id || ""),
    () => requestGetThread(id || ""),
    {
      enabled: !!id,
    }
  );
  const { data: tagsData } = useQuery(threadTagsQueryKey, () =>
    requestGetThreadTags(id || "")
  );
  const createdDate = data?.fields?.created ? new Date(data.fields.created) : null;

  // Format the date as "year month date" if it's valid
  const formattedDate = createdDate
    ? `${createdDate.getFullYear()} ${createdDate.toLocaleString('default', { month: 'long' })} ${createdDate.getDate()}`
    : 'Invalid Date';
  return (
    <Box>
      <LoadingOverlay visible={isLoading} />
      <Group position="apart">
        <Box>
          <Title fw={400}>{data?.fields?.title}</Title>
          <Text fz="xs">Asked at {formattedDate}</Text>
        </Box>
        <Box>
          <NavLink to="/question/create">
            <Button>Ask question</Button>
          </NavLink>
        </Box>
      </Group>
      <Paper withBorder p="xl" mb="xl">
        <Group align="start">
          <Box>{id && <ThreadVotes id={id} />}</Box>
          <Box sx={{ flex: 1 }}>
            <Stack align="start">
              {data?.fields?.creator_id && (
                <UserAvatar id={data?.fields?.creator_id} />
              )}
              <Box>
                {data?.fields?.content && (
                  <div
                    dangerouslySetInnerHTML={{
                      __html: data.fields.content,
                    }}
                  />
                )}
              </Box>
              {data?.fields?.category && (
                <ThreadCategory id={data.fields.category} />
              )}
              <Group spacing="sm">
                {tagsData &&
                  tagsData.results.map((tagModel) => (
                    <Badge key={tagModel.pk}>{tagModel.fields.tag_name}</Badge>
                  ))}
              </Group>
              <Group>
                Approved by:{" "}
                {data?.fields?.approver_name || data?.fields?.approver_email}
              </Group>
              <Group>
                <Button className="bg-blue-500 text-white border-blue-500">
                  Report
                </Button>
              </Group>
            </Stack>
          </Box>
        </Group>
      </Paper>
      {id && <ThreadAnswers id={id} />}
      {id && <AnswerForm id={id} title="Your answer" />}
    </Box>
  );
}
