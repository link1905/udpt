import { ActionIcon, Stack, Text } from "@mantine/core";
import { IconThumbDown, IconThumbUp } from "@tabler/icons-react";
import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query";
import {
  getThreadVotesKey,
  requestGetThreadVotes,
} from "../../services/forum/get-thread-votes.ts";
import { requestCreateThreadVote } from "../../services/forum/create-thread-vote.ts";
import {
  authRequestQueryKey,
  requestAuthRefresh,
} from "../../services/account/auth-refresh.ts";
import { requestDeleteThreadVote } from "../../services/forum/delete-thread-vote.ts";

export function ThreadVotes({ id }: { id: string | number }) {
  const queryClient = useQueryClient();

  const { data: userData } = useQuery(authRequestQueryKey, requestAuthRefresh, {
    retry: 0,
  });

  const { data } = useQuery(
    getThreadVotesKey(id),
    () => requestGetThreadVotes(id),
    {
      enabled: !!id,
    },
  );

  const count = (data?.results || []).reduce((sum, model) => {
    return sum + (model.fields.is_upvote ? 1 : -1);
  }, 0);

  const { mutate } = useMutation(requestCreateThreadVote, {
    onSuccess() {
      return queryClient.invalidateQueries(getThreadVotesKey(id));
    },
  });

  const { mutate: mutate2 } = useMutation(requestDeleteThreadVote, {
    onSuccess() {
      return queryClient.invalidateQueries(getThreadVotesKey(id));
    },
  });

  const upvoteId = data?.results?.find?.(
    (t) => t.fields.user_id === userData?.pk && t.fields.is_upvote,
  )?.pk;

  const downVoteId = data?.results?.find?.(
    (t) => t.fields.user_id === userData?.pk && !t.fields.is_upvote,
  )?.pk;

  return (
    <Stack align="center">
      <ActionIcon
        color={upvoteId ? "blue" : undefined}
        size="lg"
        radius="xl"
        variant="outline"
        onClick={() => {
          if (downVoteId) {
            mutate2(downVoteId);
          }
          !upvoteId
            ? mutate({
                thread: Number(id),
                is_upvote: true,
              })
            : mutate2(upvoteId);
        }}
      >
        <IconThumbUp size="1.625rem" />
      </ActionIcon>
      <Text fz="lg" fw={600}>
        {count}
      </Text>
      <ActionIcon
        color={downVoteId ? "blue" : undefined}
        size="lg"
        radius="xl"
        variant="outline"
        onClick={() => {
          if (upvoteId) {
            mutate2(upvoteId);
          }
          !downVoteId
            ? mutate({
                thread: Number(id),
                is_upvote: false,
              })
            : mutate2(downVoteId);
        }}
      >
        <IconThumbDown size="1.625rem" />
      </ActionIcon>
    </Stack>
  );
}
