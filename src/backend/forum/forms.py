from django import forms
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from forum.models import Thread, ThreadVote

User = get_user_model()


class ThreadForm(forms.ModelForm):
    parent = forms.ModelChoiceField(
        Thread.objects.live().filter(
            Thread.objects.question_q() | Thread.objects.answer_q()
        ),
        required=False,
    )

    def _pre_clean_creator_fields(self) -> None:
        if self.instance.pk is not None:
            self["creator_type"].field.disabled = True
            self["creator_id"].field.disabled = True

    def _pre_clean_parent_fields(self) -> None:
        if self.instance.pk is not None:
            self["parent"].field.disabled = True

    def _post_clean_body_fields(self) -> None:
        if self.has_changed:
            self.instance.approver_type = None
            self.instance.approver_id = None
            self.instance.approved = False
            self.instance.approver_name = ""
            self.instance.approver_email = ""

    def _clean_fields(self) -> None:
        self._pre_clean_creator_fields()
        self._pre_clean_parent_fields()
        super()._clean_fields()

        if self.errors:
            return

        self._post_clean_body_fields()

    class Meta:
        model = Thread
        fields = (
            "title",
            "content",
            "creator_type",
            "creator_id",
            "parent",
            "tags",
        )


class ThreadStaffForm(forms.ModelForm):
    def _pre_clean_approver_fields(self) -> None:
        if self.instance.pk is None or self.instance.approved:
            self["approved"].field.disabled = True
            self["approver_type"].field.disabled = True
            self["approver_id"].field.disabled = True

    def _post_clean_ensure_approver_fields(self) -> None:
        if self.cleaned_data["approved"] and (
            not self.cleaned_data["approver_type"]
            or not self.cleaned_data["approver_id"]
        ):
            self.add_error(
                "approver",
                ValidationError(
                    "an approver is required to approve a thread", code="required"
                ),
            )

        approver = self.cleaned_data["approver_type"].get_object_for_this_type(
            id=self.cleaned_data["approver_id"]
        )
        if approver:
            if not approver.is_staff and not approver.is_superuser:
                self.add_error(
                    "approver",
                    ValidationError(
                        "only staff members can approve threads", code="staff_only"
                    ),
                )

            self.instance.approver_name = approver.get_full_name()
            self.instance.approver_email = approver.email

    def _clean_fields(self) -> None:
        self._pre_clean_approver_fields()
        super()._clean_fields()

        if self.errors:
            return

        self._post_clean_ensure_approver_fields()

    class Meta:
        model = Thread
        fields = (
            "title",
            "content",
            "tags",
            "approved",
            "approver_type",
            "approver_id",
        )


class ThreadVoteForm(forms.ModelForm):
    thread = forms.ModelChoiceField(
        Thread.objects.live(),
        required=True,
    )

    def _pre_clean_user_fields(self) -> None:
        if self.instance.pk is not None:
            self["user_type"].field.disabled = True
            self["user_id"].field.disabled = True

    def _pre_clean_thread_fields(self) -> None:
        if self.instance.pk is not None:
            self["thread"].field.disabled = True

    def _post_clean_ensure_user_fields(self) -> None:
        user = self.cleaned_data["user_type"].get_object_for_this_type(
            id=self.cleaned_data["user_id"]
        )
        self.instance.user = user
        self.instance.user_name = user.get_full_name()
        self.instance.user_email = user.email

    def _clean_fields(self) -> None:
        self._pre_clean_user_fields()
        self._pre_clean_thread_fields()
        super()._clean_fields()

        if self.errors:
            return

        self._post_clean_ensure_user_fields()

    class Meta:
        model = ThreadVote
        fields = (
            "user_type",
            "user_id",
            "thread",
            "is_upvote",
        )
